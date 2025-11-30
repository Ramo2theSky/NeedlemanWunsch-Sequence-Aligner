from Bio import SeqIO

# Test baca file 1
records1 = list(SeqIO.parse("data\\sequence1.fasta", "fasta"))
seq1 = records1[0]
print(f"✓ Seq1: {seq1.id}")
print(f"  Panjang: {len(seq1.seq)} bp")
print(f"  Preview: {str(seq1.seq)[:80]}...")

# Test baca file 2
records2 = list(SeqIO.parse("data\\sequence2.fasta", "fasta"))
seq2 = records2[0]
print(f"\n✓ Seq2: {seq2.id}")
print(f"  Panjang: {len(seq2.seq)} bp")
print(f"  Preview: {str(seq2.seq)[:80]}...")

print("\n✓ Kedua file FASTA berhasil dibaca!")
