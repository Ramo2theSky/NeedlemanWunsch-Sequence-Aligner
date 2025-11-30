#!/usr/bin/env python
"""
Batch Analysis Script

Process multiple FASTA files for sequence alignment analysis.
Useful for comparing many sequences against a reference.

Usage:
    python batch_analysis.py -ref reference.fasta -dir sequences/ -o output/
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
from nw_alignment import NWAligner
from nw_alignment.parser import read_fasta, read_multiple_fasta
from nw_alignment.utils import export_results, print_alignment_summary


def batch_align(reference_file, sequence_dir, output_dir, match=2, mismatch=-1, gap=-2):
    """
    Align reference sequence against all sequences in a directory.
    
    Args:
        reference_file (str): Path to reference FASTA file
        sequence_dir (str): Directory containing FASTA files to align
        output_dir (str): Directory to save results
        match (int): Match score
        mismatch (int): Mismatch penalty
        gap (int): Gap penalty
    """
    ref_id, ref_seq, _ = read_fasta(reference_file)
    
    sequence_dir = Path(sequence_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    fasta_files = list(sequence_dir.glob('*.fasta')) + list(sequence_dir.glob('*.fa'))
    
    print(f"\nFound {len(fasta_files)} FASTA files")
    print(f"Reference: {ref_id}\n")
    
    aligner = NWAligner(match=match, mismatch=mismatch, gap=gap)
    results = []
    
    for i, fasta_file in enumerate(fasta_files, 1):
        try:
            seq_id, seq, _ = read_fasta(str(fasta_file))
            result = aligner.align(ref_seq, seq)
            results.append({
                'file': fasta_file.name,
                'seq_id': seq_id,
                'result': result
            })
            
            identity = result['alignment_stats']['identity']
            score = result['alignment_stats']['score']
            
            print(f"[{i}/{len(fasta_files)}] {seq_id}")
            print(f"  Score: {score:.1f} | Identity: {identity:.2f}%")
            
            # Save individual results
            export_results(result, str(output_dir), f'{seq_id}_alignment')
        
        except Exception as e:
            print(f"[{i}/{len(fasta_files)}] {fasta_file.name} - ERROR: {e}")
    
    print(f"\n✓ Batch analysis complete. Results saved to: {output_dir}/")
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch alignment analysis')
    parser.add_argument('-ref', '--reference', required=True, 
                       help='Reference FASTA file')
    parser.add_argument('-dir', '--directory', required=True,
                       help='Directory with FASTA files')
    parser.add_argument('-o', '--output', default='batch_output/',
                       help='Output directory')
    
    args = parser.parse_args()
    
    batch_align(args.reference, args.directory, args.output)
