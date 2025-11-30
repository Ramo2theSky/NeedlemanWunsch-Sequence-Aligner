"""
Tests for FASTA parser module
"""

import pytest
from pathlib import Path
from nw_alignment.parser import (
    read_fasta, read_multiple_fasta, write_fasta, validate_fasta
)


class TestReadFASTA:
    """Test read_fasta function"""
    
    def test_read_simple_fasta(self, tmp_path):
        """Test reading a simple FASTA file"""
        fasta_file = tmp_path / "test.fasta"
        fasta_file.write_text(">seq1 description\nATGC\n")
        
        seq_id, seq, description = read_fasta(str(fasta_file))
        
        assert seq_id == "seq1"
        assert seq == "ATGC"
        assert "description" in description
    
    def test_read_multiline_fasta(self, tmp_path):
        """Test reading FASTA with multiline sequence"""
        fasta_file = tmp_path / "test.fasta"
        fasta_file.write_text(">seq1\nATGC\nGATT\n")
        
        seq_id, seq, desc = read_fasta(str(fasta_file))
        
        assert seq == "ATGCGATT"
    
    def test_file_not_found(self):
        """Test handling of missing file"""
        with pytest.raises(FileNotFoundError):
            read_fasta("nonexistent.fasta")
    
    def test_empty_file(self, tmp_path):
        """Test handling of empty FASTA file"""
        fasta_file = tmp_path / "empty.fasta"
        fasta_file.write_text("")
        
        with pytest.raises(ValueError):
            read_fasta(str(fasta_file))


class TestWriteFASTA:
    """Test write_fasta function"""
    
    def test_write_simple_fasta(self, tmp_path):
        """Test writing a simple FASTA file"""
        output_file = tmp_path / "output.fasta"
        
        write_fasta(str(output_file), "seq1", "ATGC", "test sequence")
        
        assert output_file.exists()
        content = output_file.read_text()
        assert ">seq1" in content
        assert "ATGC" in content
    
    def test_write_long_sequence(self, tmp_path):
        """Test writing long sequence with line wrapping"""
        output_file = tmp_path / "output.fasta"
        long_seq = "ATGC" * 100  # 400 bp
        
        write_fasta(str(output_file), "long_seq", long_seq, line_width=60)
        
        content = output_file.read_text()
        lines = content.strip().split('\n')
        
        # First line is header, rest are sequence with max 60 chars
        for line in lines[1:]:
            assert len(line) <= 60


class TestValidateFASTA:
    """Test validate_fasta function"""
    
    def test_validate_valid_file(self, tmp_path):
        """Test validation of valid FASTA file"""
        fasta_file = tmp_path / "test.fasta"
        fasta_file.write_text(">seq1\nATGC\n")
        
        stats = validate_fasta(str(fasta_file))
        
        assert stats['num_sequences'] == 1
        assert stats['total_length'] == 4
        assert stats['min_length'] == 4
        assert stats['max_length'] == 4
    
    def test_validate_multiple_sequences(self, tmp_path):
        """Test validation with multiple sequences"""
        fasta_file = tmp_path / "multi.fasta"
        fasta_file.write_text(">seq1\nATGC\n>seq2\nGATT\nAGCC\n")
        
        stats = validate_fasta(str(fasta_file))
        
        assert stats['num_sequences'] == 2
        assert stats['total_length'] == 12
        assert stats['average_length'] == 6


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
