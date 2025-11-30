#!/usr/bin/env python
"""
Needleman-Wunsch Algorithm - Simplified Main Script

This script automatically detects FASTA files from the data/ folder
and runs the alignment without requiring command-line arguments.

Usage:
    python main.py
    
OR with optional custom parameters:
    python main.py -m 3 -ms -2 -g -3 -v

Features:
  [+] Auto-detect FASTA files from data/ folder
  [+] No need to specify file paths
  [+] Simple one-command execution
  [+] Optional parameter customization
  [+] Generates all outputs (JSON, TXT, PNG)
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime
import glob

sys.path.insert(0, str(Path(__file__).parent.parent))

from nw_alignment import NWAligner
from nw_alignment.parser import read_fasta
from nw_alignment.utils import print_alignment_summary, export_results
from nw_alignment.visualization import (
    plot_alignment_statistics,
    plot_percentage_distribution,
    plot_gap_analysis
)


def find_fasta_files(data_dir='data'):
    """Auto-detect FASTA files from data folder"""
    # If data_dir is relative, resolve from parent directory
    data_path = Path(data_dir)
    
    # If not absolute and not found, try from parent directory
    if not data_path.is_absolute() and not data_path.exists():
        parent_data_path = Path(__file__).parent.parent / data_dir
        if parent_data_path.exists():
            data_path = parent_data_path
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data folder not found: {data_dir}")
    
    fasta_files = list(data_path.glob('*.fasta')) + list(data_path.glob('*.fa'))
    
    if not fasta_files:
        raise FileNotFoundError(f"No FASTA files found in {data_path}")
    
    if len(fasta_files) < 2:
        raise ValueError(f"Need at least 2 FASTA files, found {len(fasta_files)}")
    
    # Sort files by name for consistent ordering
    fasta_files.sort()
    
    return str(fasta_files[0]), str(fasta_files[1])


def main():
    parser = argparse.ArgumentParser(
        description='Needleman-Wunsch Algorithm - Auto-detect FASTA files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          (Default parameters)
  python main.py -v                       (With visualizations)
  python main.py -m 3 -ms -2 -g -3 -v    (Custom scoring)
  python main.py -o my_results -v        (Custom output folder)
        """
    )
    
    parser.add_argument('-o', '--output', default='output', help='Output directory (default: output)')
    parser.add_argument('-m', '--match', type=int, default=2, help='Match score (default: 2)')
    parser.add_argument('-ms', '--mismatch', type=int, default=-1, help='Mismatch penalty (default: -1)')
    parser.add_argument('-g', '--gap', type=int, default=-2, help='Gap penalty (default: -2)')
    parser.add_argument('-v', '--visualize', action='store_true', help='Create visualization charts')
    parser.add_argument('-d', '--data', default='data', help='Data folder (default: data)')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("NEEDLEMAN-WUNSCH ALGORITHM - SEQUENCE ALIGNMENT")
    print("="*80)
    
    # STEP 1: Auto-detect FASTA files
    try:
        print("\n[STEP 1] Auto-detecting FASTA files...")
        seq1_file, seq2_file = find_fasta_files(args.data)
        
        seq1_id, seq1, _ = read_fasta(seq1_file)
        seq2_id, seq2, _ = read_fasta(seq2_file)
        
        print(f"  [+] File 1: {Path(seq1_file).name}")
        print(f"      ID: {seq1_id} | Length: {len(seq1)} bp")
        print(f"  [+] File 2: {Path(seq2_file).name}")
        print(f"      ID: {seq2_id} | Length: {len(seq2)} bp")
        
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1
    
    # STEP 2: Run NW Algorithm
    try:
        print(f"\n[STEP 2] Performing Needleman-Wunsch alignment...")
        print(f"  Parameters: match={args.match}, mismatch={args.mismatch}, gap={args.gap}")
        
        aligner = NWAligner(match=args.match, mismatch=args.mismatch, gap=args.gap)
        result = aligner.align(seq1, seq2)
        
        print(f"  [+] Alignment complete!")
        print(f"  [+] Alignment Score: {result['score']}")
        print(f"  [+] Identity: {result['alignment_stats']['identity']:.2f}%")
        print(f"  [+] Matches: {result['alignment_stats']['matches']}")
        print(f"  [+] Mismatches: {result['alignment_stats']['mismatches']}")
        print(f"  [+] Gaps: {result['alignment_stats']['gaps']}")
        
    except Exception as e:
        print(f"[-] Error during alignment: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1
    
    # STEP 3: Export Results
    try:
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        print(f"\n[STEP 3] Exporting results...")
        export_results(result, str(output_dir))
        print(f"  [+] Results exported to: {output_dir}/")
        print(f"      - nw_alignment_result.json")
        print(f"      - nw_alignment_result.txt")
        
    except Exception as e:
        print(f"[-] Error during export: {e}", file=sys.stderr)
        return 1
    
    # STEP 4: Create Visualizations (optional)
    if args.visualize:
        try:
            print(f"\n[STEP 4] Creating visualizations...")
            
            plot_alignment_statistics(result, str(output_dir / 'alignment_statistics.png'))
            print(f"  [+] Created: alignment_statistics.png")
            
            plot_percentage_distribution(result, str(output_dir / 'alignment_percentage.png'))
            print(f"  [+] Created: alignment_percentage.png")
            
            plot_gap_analysis(result, str(output_dir / 'alignment_gap_analysis.png'))
            print(f"  [+] Created: alignment_gap_analysis.png")
            
        except Exception as e:
            print(f"[-] Warning: Visualization failed: {e}", file=sys.stderr)
    
    # STEP 5: Print Summary
    try:
        print(f"\n[STEP 5] Summary Statistics")
        print("-" * 80)
        print_alignment_summary(result)
        
        print("\n" + "="*80)
        print("[+] ALIGNMENT COMPLETE - All files saved!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())