"""
Unit Tests for NW Alignment Module

Run tests with:
    pytest tests/
    pytest --cov=nw_alignment tests/
"""

import pytest
from pathlib import Path
from nw_alignment import NWAligner
from nw_alignment.parser import read_fasta, validate_fasta


class TestNWAligner:
    """Test cases for NWAligner class"""
    
    def test_simple_alignment(self):
        """Test basic alignment with identical sequences"""
        aligner = NWAligner()
        seq1 = "ATGC"
        seq2 = "ATGC"
        
        result = aligner.align(seq1, seq2)
        
        assert result['alignment_stats']['identity'] == 100.0
        assert result['alignment_stats']['matches'] == 4
        assert result['alignment_stats']['mismatches'] == 0
    
    def test_mismatches(self):
        """Test alignment with mismatches"""
        aligner = NWAligner()
        seq1 = "ATGC"
        seq2 = "AGGC"
        
        result = aligner.align(seq1, seq2)
        
        assert result['alignment_stats']['mismatches'] > 0
        assert result['alignment_stats']['identity'] < 100.0
    
    def test_with_gaps(self):
        """Test alignment with gaps"""
        aligner = NWAligner()
        seq1 = "ATGC"
        seq2 = "ATG"
        
        result = aligner.align(seq1, seq2)
        
        assert result['alignment_stats']['gaps'] > 0
        assert result['alignment_stats']['identity'] < 100.0
    
    def test_custom_scoring(self):
        """Test with custom scoring parameters"""
        aligner_lenient = NWAligner(match=5, mismatch=-1, gap=-1)
        aligner_strict = NWAligner(match=1, mismatch=-5, gap=-5)
        
        seq1 = "ATGC"
        seq2 = "AGCC"
        
        result_lenient = aligner_lenient.align(seq1, seq2)
        result_strict = aligner_strict.align(seq1, seq2)
        
        assert result_lenient['alignment_stats']['score'] != result_strict['alignment_stats']['score']
    
    def test_case_insensitivity(self):
        """Test that sequences are converted to uppercase"""
        aligner = NWAligner()
        seq1 = "atgc"
        seq2 = "atgc"
        
        result = aligner.align(seq1, seq2)
        
        assert result['alignment_stats']['identity'] == 100.0
    
    def test_format_alignment(self):
        """Test alignment formatting"""
        aligner = NWAligner()
        seq1 = "ATGC"
        seq2 = "ATGC"
        
        result = aligner.align(seq1, seq2)
        formatted = aligner.format_alignment(result)
        
        assert "Seq1:" in formatted
        assert "Seq2:" in formatted
        assert "|" in formatted  # Should contain match indicators
    
    def test_empty_sequences(self):
        """Test handling of empty sequences"""
        aligner = NWAligner()
        
        with pytest.raises(ValueError):
            aligner.align("", "ATGC")


class TestFASTAParser:
    """Test cases for FASTA parser functions"""
    
    def test_read_fasta_exists(self, tmp_path):
        """Test reading existing FASTA file"""
        fasta_file = tmp_path / "test.fasta"
        fasta_file.write_text(">seq1\nATGC\n")
        
        seq_id, seq, desc = read_fasta(str(fasta_file))
        
        assert seq_id == "seq1"
        assert seq == "ATGC"
    
    def test_read_fasta_not_exists(self):
        """Test reading non-existent FASTA file"""
        with pytest.raises(FileNotFoundError):
            read_fasta("nonexistent.fasta")
    
    def test_validate_fasta(self, tmp_path):
        """Test FASTA validation"""
        fasta_file = tmp_path / "test.fasta"
        fasta_file.write_text(">seq1\nATGC\n")
        
        stats = validate_fasta(str(fasta_file))
        
        assert stats['num_sequences'] == 1
        assert stats['total_length'] == 4


class TestIntegration:
    """Integration tests with real files"""
    
    def test_full_workflow(self, tmp_path):
        """Test complete alignment workflow"""
        # Create test files
        fasta1 = tmp_path / "seq1.fasta"
        fasta2 = tmp_path / "seq2.fasta"
        
        fasta1.write_text(">sequence1\nGATTACA\n")
        fasta2.write_text(">sequence2\nGCATGCU\n")
        
        # Load and align
        seq1_id, seq1, _ = read_fasta(str(fasta1))
        seq2_id, seq2, _ = read_fasta(str(fasta2))
        
        aligner = NWAligner()
        result = aligner.align(seq1, seq2)
        
        # Verify result structure
        assert 'aligned_seq1' in result
        assert 'aligned_seq2' in result
        assert 'score' in result
        assert 'alignment_stats' in result
        
        # Save results
        output_file = tmp_path / "alignment.json"
        aligner.save_result_json(result, str(output_file))
        
        assert output_file.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
