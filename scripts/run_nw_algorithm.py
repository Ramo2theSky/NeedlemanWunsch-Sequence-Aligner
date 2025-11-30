#!/usr/bin/env python
"""
Needleman-Wunsch Algorithm - Main Script

This is the RECOMMENDED approach for processing full FASTA files without 
RAM limitations. Use this for production-grade sequence alignment analysis.

Features:
  [+] Processes entire FASTA files (no memory constraints)
  [+] Professional output formatting
  [+] Multiple export formats (JSON, TXT, PNG)
  [+] Detailed statistics and visualization
  [+] Command-line interface

Usage:
    python run_nw_algorithm.py -s1 sequence1.fasta -s2 sequence2.fasta

For more information, see: docs/USAGE.md
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from nw_alignment import NWAligner
from nw_alignment.parser import read_fasta
from nw_alignment.utils import print_alignment_summary, export_results
from nw_alignment.visualization import (
    plot_alignment_statistics,
    plot_percentage_distribution,
    plot_gap_analysis
)


def main():
    parser = argparse.ArgumentParser(
        description='Needleman-Wunsch Algorithm for Global Sequence Alignment'
    )
    
    parser.add_argument('-s1', '--seq1', required=True, help='Path to first FASTA file')
    parser.add_argument('-s2', '--seq2', required=True, help='Path to second FASTA file')
    parser.add_argument('-o', '--output', default='output', help='Output directory')
    parser.add_argument('-m', '--match', type=int, default=2, help='Match score')
    parser.add_argument('-ms', '--mismatch', type=int, default=-1, help='Mismatch penalty')
    parser.add_argument('-g', '--gap', type=int, default=-2, help='Gap penalty')
    parser.add_argument('-v', '--visualize', action='store_true', help='Create visualizations')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("NEEDLEMAN-WUNSCH ALGORITHM - SEQUENCE ALIGNMENT")
    print("="*80)
    
    try:
        print("\n[STEP 1] Validating input FASTA files...")
        
        seq1_file = Path(args.seq1)
        seq2_file = Path(args.seq2)
        
        if not seq1_file.exists() or not seq2_file.exists():
            raise FileNotFoundError("One or both files not found")
        
        seq1_id, seq1, _ = read_fasta(str(seq1_file))
        seq2_id, seq2, _ = read_fasta(str(seq2_file))
        
        print(f"  [+] Seq1: {seq1_id} ({len(seq1)} bp)")
        print(f"  [+] Seq2: {seq2_id} ({len(seq2)} bp)")
        
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1
    
    try:
        print(f"\n[STEP 2] Performing Needleman-Wunsch alignment...")
        aligner = NWAligner(match=args.match, mismatch=args.mismatch, gap=args.gap)
        result = aligner.align(seq1, seq2)
        
        print(f"  [+] Alignment complete!")
        print(f"  [+] Score: {result['score']}")
        print(f"  [+] Identity: {result['alignment_stats']['identity']:.2f}%")
        
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1
    
    try:
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        print(f"\n[STEP 3] Exporting results...")
        export_results(result, str(output_dir))
        print(f"  [+] Results saved to: {output_dir}/")
        
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1
    
    if args.visualize:
        try:
            print(f"\n[STEP 4] Creating visualizations...")
            plot_alignment_statistics(result, str(output_dir / 'alignment_statistics.png'))
            plot_percentage_distribution(result, str(output_dir / 'alignment_percentage.png'))
            plot_gap_analysis(result, str(output_dir / 'alignment_gap_analysis.png'))
            print(f"  [+] Visualizations created successfully")
        except Exception as e:
            print(f"[-] Error: {e}", file=sys.stderr)
    
    try:
        print(f"\n[STEP 5] Summary Statistics")
        print_alignment_summary(result)
        print("\n" + "="*80)
        print("[+] ALIGNMENT COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
