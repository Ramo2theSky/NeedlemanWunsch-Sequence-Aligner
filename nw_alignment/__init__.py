"""
Needleman-Wunsch Algorithm Package

A Python implementation of the Needleman-Wunsch algorithm for global 
pairwise sequence alignment using BioPython.

Classes:
    - alignment.NWAligner: Main alignment class
    
Functions:
    - parser.read_fasta: Parse FASTA files
    - visualization.plot_results: Create visualization plots
    
Example:
    >>> from nw_alignment import NWAligner
    >>> aligner = NWAligner(match=2, mismatch=-1, gap=-2)
    >>> result = aligner.align("ATGC", "ATGC")
    >>> print(result['identity'])
    100.0
"""

__version__ = "1.0.0"
__author__ = "Ramo2theSky"
__license__ = "MIT"

from .alignment import NWAligner
from .parser import read_fasta, write_fasta
from .visualization import plot_alignment_statistics

__all__ = [
    "NWAligner",
    "read_fasta",
    "write_fasta",
    "plot_alignment_statistics",
]
