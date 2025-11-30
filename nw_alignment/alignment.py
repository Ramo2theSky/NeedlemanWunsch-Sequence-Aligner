"""
Needleman-Wunsch Algorithm Implementation

This module contains the core implementation of the Needleman-Wunsch 
global pairwise sequence alignment algorithm using BioPython.
"""

import Bio.pairwise2 as pairwise2
from typing import Dict, Tuple, List
import json


class NWAligner:
    """
    Needleman-Wunsch Algorithm for Global Pairwise Sequence Alignment.
    
    This class implements the Needleman-Wunsch algorithm using dynamic 
    programming to find the optimal global alignment of two sequences.
    
    Attributes:
        match_score (int): Score for matching nucleotides (default: 2)
        mismatch_score (int): Penalty for mismatches (default: -1)
        gap_penalty (int): Penalty for gaps/indels (default: -2)
    
    Example:
        >>> aligner = NWAligner(match=2, mismatch=-1, gap=-2)
        >>> seq1 = "GATTACA"
        >>> seq2 = "GCATGCU"
        >>> result = aligner.align(seq1, seq2)
        >>> print(f"Identity: {result['identity']:.2f}%")
        Identity: 71.43%
    """
    
    def __init__(self, match: int = 2, mismatch: int = -1, gap: int = -2):
        """
        Initialize the NW Aligner with scoring parameters.
        
        Args:
            match (int): Score for matching nucleotides. Default is 2.
            mismatch (int): Penalty for mismatches. Default is -1.
            gap (int): Penalty for gaps/indels. Default is -2.
        """
        self.match_score = match
        self.mismatch_score = mismatch
        self.gap_penalty = gap
    
    def align(self, seq1: str, seq2: str) -> Dict:
        """
        Perform Needleman-Wunsch alignment on two sequences.
        
        Args:
            seq1 (str): First DNA/protein sequence
            seq2 (str): Second DNA/protein sequence
            
        Returns:
            dict: Dictionary containing alignment results with keys:
                - 'seq1_id': First sequence identifier
                - 'seq2_id': Second sequence identifier
                - 'aligned_seq1': Aligned first sequence
                - 'aligned_seq2': Aligned second sequence
                - 'score': Alignment score
                - 'matches': Number of matching positions
                - 'mismatches': Number of mismatching positions
                - 'gaps': Total number of gaps
                - 'identity': Identity percentage
                - 'length': Alignment length
                - 'alignment_stats': Detailed statistics dictionary
        """
        # Convert to uppercase
        seq1 = str(seq1).upper()
        seq2 = str(seq2).upper()
        
        # Perform alignment using BioPython's globalms
        alignments = pairwise2.align.globalms(
            seq1, seq2,
            self.match_score,      # Match score
            self.mismatch_score,   # Mismatch penalty
            self.gap_penalty,      # Gap open penalty
            self.gap_penalty       # Gap extension penalty
        )
        
        if not alignments:
            raise ValueError("No alignment found")
        
        # Get best alignment (highest score)
        best_alignment = alignments[0]
        aligned_seq1, aligned_seq2, score, begin, end = best_alignment
        
        # Calculate statistics
        stats = self._calculate_statistics(aligned_seq1, aligned_seq2, score)
        
        return {
            'aligned_seq1': aligned_seq1,
            'aligned_seq2': aligned_seq2,
            'score': score,
            'matches': stats['matches'],
            'mismatches': stats['mismatches'],
            'gaps': stats['gaps'],
            'gaps_seq1': stats['gaps_seq1'],
            'gaps_seq2': stats['gaps_seq2'],
            'identity': stats['identity'],
            'length': stats['length'],
            'alignment_stats': stats
        }
    
    def _calculate_statistics(self, aligned_seq1: str, aligned_seq2: str, 
                             score: float) -> Dict:
        """
        Calculate detailed statistics from aligned sequences.
        
        Args:
            aligned_seq1 (str): First aligned sequence
            aligned_seq2 (str): Second aligned sequence
            score (float): Alignment score
            
        Returns:
            dict: Statistics dictionary with computed metrics
        """
        length = len(aligned_seq1)
        matches = sum(1 for s1, s2 in zip(aligned_seq1, aligned_seq2) if s1 == s2)
        gaps_seq1 = aligned_seq1.count('-')
        gaps_seq2 = aligned_seq2.count('-')
        total_gaps = gaps_seq1 + gaps_seq2
        
        # Mismatches = positions that differ (excluding gaps)
        mismatches = sum(
            1 for s1, s2 in zip(aligned_seq1, aligned_seq2) 
            if s1 != s2 and s1 != '-' and s2 != '-'
        )
        
        identity = (matches / length * 100) if length > 0 else 0
        gap_percentage = (total_gaps / (length * 2) * 100) if length > 0 else 0
        
        return {
            'matches': matches,
            'mismatches': mismatches,
            'gaps': total_gaps,
            'gaps_seq1': gaps_seq1,
            'gaps_seq2': gaps_seq2,
            'identity': identity,
            'length': length,
            'score': score,
            'gap_percentage': gap_percentage,
            'match_percentage': (matches / length * 100) if length > 0 else 0,
            'mismatch_percentage': (mismatches / length * 100) if length > 0 else 0
        }
    
    def format_alignment(self, result: Dict, line_width: int = 60) -> str:
        """
        Format alignment result for display.
        
        Args:
            result (dict): Alignment result from align()
            line_width (int): Number of characters per line
            
        Returns:
            str: Formatted alignment string
        """
        seq1 = result['aligned_seq1']
        seq2 = result['aligned_seq2']
        
        output = []
        output.append("=" * 100)
        output.append("PAIRWISE ALIGNMENT")
        output.append("=" * 100)
        output.append("")
        
        for i in range(0, len(seq1), line_width):
            seq1_block = seq1[i:i+line_width]
            seq2_block = seq2[i:i+line_width]
            
            # Create match indicator line
            match_line = ""
            for s1, s2 in zip(seq1_block, seq2_block):
                if s1 == s2:
                    match_line += "|"
                elif s1 == "-" or s2 == "-":
                    match_line += " "
                else:
                    match_line += "."
            
            output.append(f"Seq1: {seq1_block}")
            output.append(f"      {match_line}")
            output.append(f"Seq2: {seq2_block}")
            output.append("")
        
        output.append("=" * 100)
        output.append("Legend: | = match, . = mismatch, (space) = gap")
        output.append("=" * 100)
        
        return "\n".join(output)
    
    def save_result_json(self, result: Dict, output_file: str):
        """
        Save alignment result to JSON file.
        
        Args:
            result (dict): Alignment result from align()
            output_file (str): Path to output JSON file
        """
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
    
    def save_result_text(self, result: Dict, output_file: str, 
                        seq1_id: str = "Seq1", seq2_id: str = "Seq2"):
        """
        Save alignment result to text file.
        
        Args:
            result (dict): Alignment result from align()
            output_file (str): Path to output text file
            seq1_id (str): Name of first sequence
            seq2_id (str): Name of second sequence
        """
        stats = result['alignment_stats']
        
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("NEEDLEMAN-WUNSCH ALIGNMENT RESULT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write("ALIGNMENT STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Score:              {stats['score']:.1f}\n")
            f.write(f"Length:             {stats['length']} bp\n")
            f.write(f"Matches:            {stats['matches']} ({stats['match_percentage']:.2f}%)\n")
            f.write(f"Mismatches:         {stats['mismatches']}\n")
            f.write(f"Gaps (Total):       {stats['gaps']}\n")
            f.write(f"  - {seq1_id} gaps:    {stats['gaps_seq1']}\n")
            f.write(f"  - {seq2_id} gaps:    {stats['gaps_seq2']}\n")
            f.write(f"Identity:           {stats['identity']:.2f}%\n")
            f.write(f"Gap Percentage:     {stats['gap_percentage']:.2f}%\n")
            f.write("\n" + "=" * 80 + "\n")
            
            f.write("ALIGNMENT\n")
            f.write("-" * 80 + "\n\n")
            f.write(self.format_alignment(result))
