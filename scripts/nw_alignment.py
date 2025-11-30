"""
Implementasi Needleman-Wunsch (NW) Algorithm menggunakan BioPython
Tugas Mata Kuliah: Bioinformatika
"""

from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import Bio.pairwise2 as pairwise2
from Bio.pairwise2 import format_alignment
import json
from pathlib import Path
from datetime import datetime


class NWAlignmentAnalyzer:
    """
    Kelas untuk melakukan alignment menggunakan Needleman-Wunsch Algorithm
    dan analisis hasil alignment
    """
    
    def __init__(self, seq1_file, seq2_file, output_dir="output"):
        """
        Inisialisasi analyzer dengan file FASTA
        
        Args:
            seq1_file: Path ke file FASTA pertama
            seq2_file: Path ke file FASTA kedua
            output_dir: Direktori untuk output
        """
        self.seq1_file = seq1_file
        self.seq2_file = seq2_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.seq1 = None
        self.seq1_id = None
        self.seq2 = None
        self.seq2_id = None
        self.alignment_result = None
        
    def read_fasta_files(self):
        """
        Membaca file FASTA dan mengekstrak sekuens
        """
        print(f"📖 Membaca file FASTA...")
        
        # Baca file pertama
        try:
            records1 = list(SeqIO.parse(self.seq1_file, "fasta"))
            if not records1:
                raise ValueError(f"File {self.seq1_file} kosong!")
            self.seq1_id = records1[0].id
            self.seq1 = str(records1[0].seq).upper()
            print(f"   ✓ Sekuens 1: {self.seq1_id} (panjang: {len(self.seq1)} bp/aa)")
        except Exception as e:
            print(f"   ✗ Error membaca file 1: {e}")
            return False
        
        # Baca file kedua
        try:
            records2 = list(SeqIO.parse(self.seq2_file, "fasta"))
            if not records2:
                raise ValueError(f"File {self.seq2_file} kosong!")
            self.seq2_id = records2[0].id
            self.seq2 = str(records2[0].seq).upper()
            print(f"   ✓ Sekuens 2: {self.seq2_id} (panjang: {len(self.seq2)} bp/aa)")
        except Exception as e:
            print(f"   ✗ Error membaca file 2: {e}")
            return False
        
        return True
    
    def perform_alignment(self, match_score=2, mismatch_score=-1, gap_penalty=-2):
        """
        Melakukan alignment menggunakan Needleman-Wunsch Algorithm
        
        Args:
            match_score: Skor untuk match
            mismatch_score: Skor untuk mismatch
            gap_penalty: Skor untuk gap (penalty)
        """
        print(f"\n🔄 Melakukan Needleman-Wunsch Alignment...")
        print(f"   Parameter:")
        print(f"   - Match score: {match_score}")
        print(f"   - Mismatch score: {mismatch_score}")
        print(f"   - Gap penalty: {gap_penalty}")
        
        # Gunakan Bio.pairwise2 untuk NW alignment
        # Pilih semua alignment dengan skor tertinggi
        alignments = pairwise2.align.globalms(
            self.seq1, 
            self.seq2, 
            match_score,           # Match score
            mismatch_score,        # Mismatch score
            gap_penalty,           # Gap open penalty
            gap_penalty            # Gap extension penalty
        )
        
        if not alignments:
            print(f"   ✗ Tidak ada alignment yang ditemukan!")
            return False
        
        # Ambil alignment dengan skor tertinggi
        self.alignment_result = alignments[0]
        print(f"   ✓ Alignment selesai!")
        print(f"   - Jumlah alignment optimal: {len(alignments)}")
        print(f"   - Skor alignment: {self.alignment_result[2]}")
        
        return True
    
    def calculate_statistics(self):
        """
        Menghitung statistik dari hasil alignment
        """
        if not self.alignment_result:
            print("   ✗ Belum ada hasil alignment!")
            return None
        
        aligned_seq1, aligned_seq2, score, begin, end = self.alignment_result
        
        # Hitung matches, mismatches, dan gaps
        matches = sum(1 for i, j in zip(aligned_seq1, aligned_seq2) if i == j)
        mismatches = sum(1 for i, j in zip(aligned_seq1, aligned_seq2) if i != j and i != '-' and j != '-')
        gaps_seq1 = aligned_seq1.count('-')
        gaps_seq2 = aligned_seq2.count('-')
        total_gaps = gaps_seq1 + gaps_seq2
        
        alignment_length = len(aligned_seq1)
        
        # Hitung persentase
        identity = (matches / alignment_length) * 100 if alignment_length > 0 else 0
        similarity = ((matches - mismatches) / alignment_length) * 100 if alignment_length > 0 else 0
        gap_percentage = (total_gaps / (alignment_length * 2)) * 100 if alignment_length > 0 else 0
        
        stats = {
            'alignment_length': alignment_length,
            'matches': matches,
            'mismatches': mismatches,
            'gaps_seq1': gaps_seq1,
            'gaps_seq2': gaps_seq2,
            'total_gaps': total_gaps,
            'identity_percent': round(identity, 2),
            'similarity_percent': round(similarity, 2),
            'gap_percentage': round(gap_percentage, 2),
            'alignment_score': score,
            'original_seq1_length': len(self.seq1),
            'original_seq2_length': len(self.seq2),
        }
        
        return stats
    
    def print_alignment(self, line_width=50):
        """
        Menampilkan hasil alignment dengan format yang rapi
        """
        if not self.alignment_result:
            print("✗ Belum ada hasil alignment!")
            return
        
        aligned_seq1, aligned_seq2, score, begin, end = self.alignment_result
        
        print(f"\n{'='*80}")
        print(f"HASIL ALIGNMENT NEEDLEMAN-WUNSCH")
        print(f"{'='*80}")
        print(f"Sekuens 1 ({self.seq1_id}): {len(self.seq1)} bp/aa")
        print(f"Sekuens 2 ({self.seq2_id}): {len(self.seq2)} bp/aa")
        print(f"Skor Alignment: {score}")
        print(f"{'='*80}\n")
        
        # Tampilkan alignment dalam blok
        for i in range(0, len(aligned_seq1), line_width):
            seq1_block = aligned_seq1[i:i+line_width]
            seq2_block = aligned_seq2[i:i+line_width]
            
            # Buat matching string
            match_block = ""
            for s1, s2 in zip(seq1_block, seq2_block):
                if s1 == s2:
                    match_block += "|"
                elif s1 == "-" or s2 == "-":
                    match_block += " "
                else:
                    match_block += "."
            
            print(f"Seq1: {seq1_block}")
            print(f"      {match_block}")
            print(f"Seq2: {seq2_block}")
            print()
    
    def print_statistics(self):
        """
        Menampilkan statistik alignment
        """
        stats = self.calculate_statistics()
        if not stats:
            return
        
        print(f"\n{'='*80}")
        print(f"STATISTIK ALIGNMENT")
        print(f"{'='*80}")
        print(f"Panjang alignment: {stats['alignment_length']} bp/aa")
        print(f"Matches: {stats['matches']} ({stats['identity_percent']}%)")
        print(f"Mismatches: {stats['mismatches']}")
        print(f"Gaps total: {stats['total_gaps']}")
        print(f"  - Gap di sekuens 1: {stats['gaps_seq1']}")
        print(f"  - Gap di sekuens 2: {stats['gaps_seq2']}")
        print(f"\nIdentity: {stats['identity_percent']}%")
        print(f"Similarity: {stats['similarity_percent']}%")
        print(f"Gap percentage: {stats['gap_percentage']}%")
        print(f"Alignment score: {stats['alignment_score']}")
        print(f"{'='*80}\n")
        
        return stats
    
    def save_results(self, filename="nw_alignment_result.txt"):
        """
        Menyimpan hasil alignment ke file text
        """
        if not self.alignment_result:
            print("✗ Belum ada hasil alignment untuk disimpan!")
            return False
        
        output_file = self.output_dir / filename
        stats = self.calculate_statistics()
        
        with open(output_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("HASIL NEEDLEMAN-WUNSCH ALIGNMENT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("INFORMASI SEKUENS\n")
            f.write("-"*80 + "\n")
            f.write(f"Sekuens 1: {self.seq1_id}\n")
            f.write(f"  Panjang: {len(self.seq1)} bp/aa\n")
            f.write(f"  Preview: {self.seq1[:100]}...\n\n")
            
            f.write(f"Sekuens 2: {self.seq2_id}\n")
            f.write(f"  Panjang: {len(self.seq2)} bp/aa\n")
            f.write(f"  Preview: {self.seq2[:100]}...\n\n")
            
            f.write("HASIL ALIGNMENT\n")
            f.write("-"*80 + "\n")
            aligned_seq1, aligned_seq2, score, begin, end = self.alignment_result
            f.write(f"Skor: {score}\n\n")
            
            # Tulis alignment dengan line wrapping
            line_width = 50
            for i in range(0, len(aligned_seq1), line_width):
                seq1_block = aligned_seq1[i:i+line_width]
                seq2_block = aligned_seq2[i:i+line_width]
                
                match_block = ""
                for s1, s2 in zip(seq1_block, seq2_block):
                    if s1 == s2:
                        match_block += "|"
                    elif s1 == "-" or s2 == "-":
                        match_block += " "
                    else:
                        match_block += "."
                
                f.write(f"Seq1: {seq1_block}\n")
                f.write(f"      {match_block}\n")
                f.write(f"Seq2: {seq2_block}\n\n")
            
            f.write("\nSTATISTIK ALIGNMENT\n")
            f.write("-"*80 + "\n")
            f.write(f"Panjang alignment: {stats['alignment_length']} bp/aa\n")
            f.write(f"Matches: {stats['matches']} ({stats['identity_percent']}%)\n")
            f.write(f"Mismatches: {stats['mismatches']}\n")
            f.write(f"Gaps total: {stats['total_gaps']}\n")
            f.write(f"  - Gap di sekuens 1: {stats['gaps_seq1']}\n")
            f.write(f"  - Gap di sekuens 2: {stats['gaps_seq2']}\n")
            f.write(f"Identity: {stats['identity_percent']}%\n")
            f.write(f"Similarity: {stats['similarity_percent']}%\n")
            f.write(f"Gap percentage: {stats['gap_percentage']}%\n")
        
        print(f"✓ Hasil disimpan ke: {output_file}")
        return True
    
    def save_json_results(self, filename="nw_alignment_result.json"):
        """
        Menyimpan hasil alignment ke format JSON
        """
        if not self.alignment_result:
            print("✗ Belum ada hasil alignment untuk disimpan!")
            return False
        
        output_file = self.output_dir / filename
        aligned_seq1, aligned_seq2, score, begin, end = self.alignment_result
        stats = self.calculate_statistics()
        
        result_data = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'algorithm': 'Needleman-Wunsch (Global Alignment)'
            },
            'sequences': {
                'seq1': {
                    'id': self.seq1_id,
                    'length': len(self.seq1),
                    'preview': self.seq1[:100]
                },
                'seq2': {
                    'id': self.seq2_id,
                    'length': len(self.seq2),
                    'preview': self.seq2[:100]
                }
            },
            'alignment': {
                'aligned_seq1': aligned_seq1,
                'aligned_seq2': aligned_seq2,
                'score': score
            },
            'statistics': stats
        }
        
        with open(output_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        print(f"✓ Hasil JSON disimpan ke: {output_file}")
        return True
    
    def run_full_analysis(self):
        """
        Menjalankan analisis lengkap
        """
        print("\n" + "="*80)
        print("IMPLEMENTASI NEEDLEMAN-WUNSCH ALGORITHM DENGAN BIOPYTHON")
        print("="*80 + "\n")
        
        if not self.read_fasta_files():
            return False
        
        if not self.perform_alignment():
            return False
        
        self.print_alignment()
        self.print_statistics()
        
        self.save_results()
        self.save_json_results()
        
        print("\n✓ Analisis selesai!\n")
        return True


if __name__ == "__main__":
    import sys
    
    # Gunakan argumen command line atau default path
    if len(sys.argv) > 2:
        seq1_file = sys.argv[1]
        seq2_file = sys.argv[2]
    else:
        # Default path (sesuaikan dengan lokasi file Anda)
        seq1_file = "data/sequence1.fasta"
        seq2_file = "data/sequence2.fasta"
    
    # Jalankan analisis
    analyzer = NWAlignmentAnalyzer(seq1_file, seq2_file, output_dir="output")
    analyzer.run_full_analysis()
