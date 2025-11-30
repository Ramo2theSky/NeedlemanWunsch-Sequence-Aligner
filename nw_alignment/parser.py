"""
FASTA File Parser

Functions for reading and writing FASTA format sequence files.
"""

from pathlib import Path
from typing import Tuple, Dict, List
from Bio import SeqIO


def read_fasta(fasta_file: str) -> Tuple[str, str, str]:
    """
    Read a FASTA file and return sequence ID and sequence.
    
    Args:
        fasta_file (str): Path to FASTA file
        
    Returns:
        tuple: (sequence_id, sequence, description)
        
    Raises:
        FileNotFoundError: If FASTA file not found
        ValueError: If FASTA file is empty
        
    Example:
        >>> seq_id, seq, desc = read_fasta("sequence.fasta")
        >>> print(f"Sequence length: {len(seq)} bp")
        Sequence length: 16480 bp
    """
    fasta_path = Path(fasta_file)
    
    if not fasta_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {fasta_file}")
    
    try:
        records = list(SeqIO.parse(str(fasta_path), "fasta"))
        
        if not records:
            raise ValueError(f"Empty FASTA file: {fasta_file}")
        
        record = records[0]
        seq_id = record.id
        sequence = str(record.seq).upper()
        description = record.description
        
        return seq_id, sequence, description
    
    except Exception as e:
        raise ValueError(f"Error reading FASTA file: {e}")


def read_multiple_fasta(fasta_file: str) -> List[Tuple[str, str, str]]:
    """
    Read a FASTA file with multiple sequences.
    
    Args:
        fasta_file (str): Path to FASTA file
        
    Returns:
        list: List of (sequence_id, sequence, description) tuples
        
    Example:
        >>> sequences = read_multiple_fasta("multi.fasta")
        >>> for seq_id, seq, desc in sequences:
        ...     print(f"{seq_id}: {len(seq)} bp")
    """
    fasta_path = Path(fasta_file)
    
    if not fasta_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {fasta_file}")
    
    results = []
    try:
        records = SeqIO.parse(str(fasta_path), "fasta")
        
        for record in records:
            seq_id = record.id
            sequence = str(record.seq).upper()
            description = record.description
            results.append((seq_id, sequence, description))
        
        if not results:
            raise ValueError(f"Empty FASTA file: {fasta_file}")
        
        return results
    
    except Exception as e:
        raise ValueError(f"Error reading FASTA file: {e}")


def write_fasta(output_file: str, seq_id: str, sequence: str, 
               description: str = "", line_width: int = 60):
    """
    Write sequence to FASTA format file.
    
    Args:
        output_file (str): Path to output FASTA file
        seq_id (str): Sequence identifier
        sequence (str): Sequence string
        description (str): Optional sequence description
        line_width (int): Characters per line (default: 60)
        
    Example:
        >>> write_fasta("output.fasta", "seq1", "ATGCATGC")
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        # Write header
        if description:
            f.write(f">{seq_id} {description}\n")
        else:
            f.write(f">{seq_id}\n")
        
        # Write sequence in chunks
        for i in range(0, len(sequence), line_width):
            f.write(sequence[i:i+line_width] + "\n")


def validate_fasta(fasta_file: str) -> Dict:
    """
    Validate FASTA file and return basic statistics.
    
    Args:
        fasta_file (str): Path to FASTA file
        
    Returns:
        dict: Statistics about FASTA file
        
    Example:
        >>> stats = validate_fasta("sequence.fasta")
        >>> print(f"Found {stats['num_sequences']} sequences")
        Found 1 sequences
    """
    fasta_path = Path(fasta_file)
    
    if not fasta_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {fasta_file}")
    
    try:
        records = list(SeqIO.parse(str(fasta_path), "fasta"))
        
        if not records:
            raise ValueError("Empty FASTA file")
        
        total_length = sum(len(record.seq) for record in records)
        
        return {
            'file': str(fasta_path),
            'num_sequences': len(records),
            'total_length': total_length,
            'average_length': total_length / len(records),
            'min_length': min(len(record.seq) for record in records),
            'max_length': max(len(record.seq) for record in records),
            'sequences': [(record.id, len(record.seq)) for record in records]
        }
    
    except Exception as e:
        raise ValueError(f"Error validating FASTA file: {e}")
