"""
Utility Functions

Helper functions for alignment analysis and data processing.
"""

from typing import Dict, List
from pathlib import Path
import json


def print_alignment_summary(result: Dict, seq1_id: str = "Seq1", 
                           seq2_id: str = "Seq2") -> None:
    """
    Print alignment summary to console.
    
    Args:
        result (dict): Alignment result from NWAligner.align()
        seq1_id (str): Name of first sequence
        seq2_id (str): Name of second sequence
    """
    stats = result['alignment_stats']
    
    print("\n" + "="*70)
    print("ALIGNMENT STATISTICS")
    print("="*70)
    print(f"\nScore:              {stats['score']:.1f}")
    print(f"Alignment Length:   {stats['length']} bp")
    print(f"\nMatches:            {stats['matches']} ({stats['match_percentage']:.2f}%)")
    print(f"Mismatches:         {stats['mismatches']} ({stats['mismatch_percentage']:.2f}%)")
    print(f"Gaps (Total):       {stats['gaps']} ({stats['gap_percentage']:.2f}%)")
    print(f"  - {seq1_id} gaps:  {stats['gaps_seq1']}")
    print(f"  - {seq2_id} gaps:  {stats['gaps_seq2']}")
    print(f"\nIdentity:           {stats['identity']:.2f}%")
    print("="*70 + "\n")


def export_results(result: Dict, output_dir: str, base_name: str = "alignment") -> Dict:
    """
    Export alignment results to multiple formats.
    
    Args:
        result (dict): Alignment result
        output_dir (str): Directory to save results
        base_name (str): Base name for output files
        
    Returns:
        dict: Paths to saved files
        
    Example:
        >>> files = export_results(result, "output/", "my_alignment")
        >>> print(files['json'])
        output/my_alignment.json
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    files = {}
    
    # Save JSON
    json_file = output_path / f"{base_name}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    files['json'] = str(json_file)
    
    # Save text alignment
    txt_file = output_path / f"{base_name}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("NEEDLEMAN-WUNSCH ALIGNMENT RESULT\n")
        f.write("="*80 + "\n\n")
        
        stats = result['alignment_stats']
        f.write("ALIGNMENT STATISTICS\n")
        f.write("-"*80 + "\n")
        f.write(f"Score:              {stats['score']:.1f}\n")
        f.write(f"Length:             {stats['length']} bp\n")
        f.write(f"Matches:            {stats['matches']} ({stats['match_percentage']:.2f}%)\n")
        f.write(f"Mismatches:         {stats['mismatches']}\n")
        f.write(f"Gaps (Total):       {stats['gaps']}\n")
        f.write(f"Identity:           {stats['identity']:.2f}%\n\n")
        
        f.write("ALIGNMENT\n")
        f.write("-"*80 + "\n\n")
        
        # Write alignment with wrapping
        seq1 = result['aligned_seq1']
        seq2 = result['aligned_seq2']
        line_width = 60
        
        for i in range(0, len(seq1), line_width):
            f.write(f"Seq1: {seq1[i:i+line_width]}\n")
            
            match_line = ""
            for s1, s2 in zip(seq1[i:i+line_width], seq2[i:i+line_width]):
                if s1 == s2:
                    match_line += "|"
                elif s1 == "-" or s2 == "-":
                    match_line += " "
                else:
                    match_line += "."
            
            f.write(f"      {match_line}\n")
            f.write(f"Seq2: {seq2[i:i+line_width]}\n\n")
    
    files['text'] = str(txt_file)
    
    print(f"[+] Results exported to: {output_dir}")
    print(f"  - JSON: {json_file.name}")
    print(f"  - Text: {txt_file.name}")
    
    return files


def interpret_identity(identity: float) -> str:
    """
    Interpret identity percentage biologically.
    
    Args:
        identity (float): Identity percentage (0-100)
        
    Returns:
        str: Biological interpretation
    """
    if identity >= 95:
        return "NEARLY IDENTICAL - Same species or very close relatives"
    elif identity >= 85:
        return "HIGHLY SIMILAR - Same genus, close species"
    elif identity >= 75:
        return "MODERATELY SIMILAR - Related species, same family"
    elif identity >= 60:
        return "SIMILAR - Different families but same order"
    elif identity >= 40:
        return "WEAK SIMILARITY - Distant relatives"
    else:
        return "HIGHLY DIVERGENT - Very distant relatives or different sequences"


def compare_multiple_alignments(results: List[Dict]) -> Dict:
    """
    Compare statistics across multiple alignments.
    
    Args:
        results (list): List of alignment results
        
    Returns:
        dict: Comparison statistics
        
    Example:
        >>> result1 = aligner.align(seq1, seq2)
        >>> result2 = aligner.align(seq1, seq3)
        >>> comparison = compare_multiple_alignments([result1, result2])
    """
    if not results:
        raise ValueError("No results to compare")
    
    identities = [r['alignment_stats']['identity'] for r in results]
    scores = [r['alignment_stats']['score'] for r in results]
    lengths = [r['alignment_stats']['length'] for r in results]
    
    return {
        'num_alignments': len(results),
        'avg_identity': sum(identities) / len(identities),
        'max_identity': max(identities),
        'min_identity': min(identities),
        'avg_score': sum(scores) / len(scores),
        'max_score': max(scores),
        'min_score': min(scores),
        'avg_length': sum(lengths) / len(lengths),
        'identities': identities,
        'scores': scores,
        'lengths': lengths
    }
