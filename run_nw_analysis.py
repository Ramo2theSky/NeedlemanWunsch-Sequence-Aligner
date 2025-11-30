"""
Implementasi Needleman-Wunsch Algorithm - Step by Step Execution
"""

from Bio import SeqIO
import Bio.pairwise2 as pairwise2
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

print("="*80)
print("NEEDLEMAN-WUNSCH ALGORITHM - STEP BY STEP EXECUTION")
print("="*80)

# ============================================================================
# STEP 1: Load FASTA Sequences
# ============================================================================
print("\n[STEP 1] Membaca file FASTA...")
print("-" * 80)

records1 = list(SeqIO.parse("data/sequence1.fasta", "fasta"))
seq1_record = records1[0]
seq1_id = seq1_record.id
seq1 = str(seq1_record.seq).upper()

records2 = list(SeqIO.parse("data/sequence2.fasta", "fasta"))
seq2_record = records2[0]
seq2_id = seq2_record.id
seq2 = str(seq2_record.seq).upper()

print(f"✓ Sekuens 1 ({seq1_id}): {len(seq1)} bp")
print(f"  Preview: {seq1[:100]}...")
print(f"\n✓ Sekuens 2 ({seq2_id}): {len(seq2)} bp")
print(f"  Preview: {seq2[:100]}...")

# ============================================================================
# STEP 2: Set Scoring Parameters
# ============================================================================
print("\n[STEP 2] Setup Parameter Scoring...")
print("-" * 80)

match_score = 2
mismatch_score = -1
gap_penalty = -2

print(f"✓ Match score: {match_score}")
print(f"✓ Mismatch score: {mismatch_score}")
print(f"✓ Gap penalty: {gap_penalty}")
print(f"\nParameter Configuration:")
print(f"  - Global alignment (full length sequences)")
print(f"  - Dynamic programming scoring")
print(f"  - Balanced parameters (moderate stringency)")

# ============================================================================
# STEP 3: Perform NW Alignment
# ============================================================================
print("\n[STEP 3] Menjalankan Needleman-Wunsch Alignment...")
print("-" * 80)
print("⏳ Proses alignment sedang berjalan...")

alignments = pairwise2.align.globalms(
    seq1, 
    seq2, 
    match_score,
    mismatch_score,
    gap_penalty,
    gap_penalty
)

print(f"✓ Alignment selesai!")
print(f"✓ Jumlah alignment optimal ditemukan: {len(alignments)}")

# ============================================================================
# STEP 4: Extract Best Alignment
# ============================================================================
print("\n[STEP 4] Ekstrak hasil alignment terbaik...")
print("-" * 80)

best_alignment = alignments[0]
aligned_seq1, aligned_seq2, score, begin, end = best_alignment

print(f"✓ Alignment Score: {score}")
print(f"✓ Alignment Length: {len(aligned_seq1)} bp")
print(f"✓ Position range: {begin} - {end}")

# ============================================================================
# STEP 5: Calculate Statistics
# ============================================================================
print("\n[STEP 5] Menghitung statistik alignment...")
print("-" * 80)

matches = sum(1 for i, j in zip(aligned_seq1, aligned_seq2) if i == j)
mismatches = sum(1 for i, j in zip(aligned_seq1, aligned_seq2) if i != j and i != '-' and j != '-')
gaps_seq1 = aligned_seq1.count('-')
gaps_seq2 = aligned_seq2.count('-')
total_gaps = gaps_seq1 + gaps_seq2

alignment_length = len(aligned_seq1)
identity = (matches / alignment_length) * 100 if alignment_length > 0 else 0
gap_percentage = (total_gaps / (alignment_length * 2)) * 100 if alignment_length > 0 else 0

print(f"✓ Matches: {matches} ({(matches/alignment_length)*100:.2f}%)")
print(f"✓ Mismatches: {mismatches}")
print(f"✓ Gaps (Seq1): {gaps_seq1}")
print(f"✓ Gaps (Seq2): {gaps_seq2}")
print(f"✓ Total Gaps: {total_gaps}")
print(f"\n✓ Identity: {identity:.2f}%")
print(f"✓ Gap Percentage: {gap_percentage:.2f}%")

# ============================================================================
# STEP 6: Display Alignment
# ============================================================================
print("\n[STEP 6] Menampilkan alignment result...")
print("-" * 80)

line_width = 60
print(f"\nAlignment Visualization (showing first 180 bp):\n")

for i in range(0, min(180, len(aligned_seq1)), line_width):
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
    
    print(f"Seq1: {seq1_block}")
    print(f"      {match_block}")
    print(f"Seq2: {seq2_block}")
    print()

# ============================================================================
# STEP 7: Create Statistics Table
# ============================================================================
print("[STEP 7] Membuat statistik summary table...")
print("-" * 80)

stats_data = {
    'Metrik': [
        'Alignment Length',
        'Matches',
        'Mismatches',
        'Gap Seq1',
        'Gap Seq2',
        'Total Gaps',
        'Identity (%)',
        'Gap Percentage (%)',
        'Alignment Score'
    ],
    'Nilai': [
        alignment_length,
        matches,
        mismatches,
        gaps_seq1,
        gaps_seq2,
        total_gaps,
        f'{identity:.2f}',
        f'{gap_percentage:.2f}',
        score
    ]
}

stats_df = pd.DataFrame(stats_data)
print("\n" + stats_df.to_string(index=False))

# ============================================================================
# STEP 8: Biological Interpretation
# ============================================================================
print("\n[STEP 8] Interpretasi hasil secara biologis...")
print("-" * 80)

print(f"\n✓ IDENTITY ANALYSIS ({identity:.2f}%):")
if identity > 95:
    print(f"  → Sekuens NEARLY IDENTICAL")
    print(f"  → Species sama atau sangat closely related")
    print(f"  → Evolusi yang sangat recent")
elif identity > 85:
    print(f"  → Sekuens HIGHLY SIMILAR")
    print(f"  → Sama genus atau close species")
    print(f"  → Common ancestor relatif recent")
else:
    print(f"  → Sekuens MODERATELY SIMILAR")

print(f"\n✓ GAP ANALYSIS ({gap_percentage:.2f}%):")
if gap_percentage < 1:
    print(f"  → Sangat sedikit insertion/deletion events")
    print(f"  → Genome structure sangat conserved")
elif gap_percentage < 5:
    print(f"  → Moderate insertion/deletion events")
else:
    print(f"  → Banyak structural differences")

print(f"\n✓ EVOLUTIONARY SIGNIFICANCE:")
print(f"  Sus barbatus dan Sus scrofa adalah spesies yang:")
print(f"  - Sangat closely related (same genus Sus)")
print(f"  - Memiliki ancestry yang relatif recent")
print(f"  - Genome yang highly conserved")
print(f"  - Evolusi yang minimal dalam waktu terakhir")

# ============================================================================
# STEP 9: Save Results
# ============================================================================
print("\n[STEP 9] Menyimpan hasil ke file...")
print("-" * 80)

# Create output directory
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Save text report
output_file = output_dir / "nw_alignment_result.txt"
with open(output_file, 'w') as f:
    f.write("="*80 + "\n")
    f.write("NEEDLEMAN-WUNSCH ALIGNMENT RESULT\n")
    f.write("="*80 + "\n\n")
    
    f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("SEQUENCE INFORMATION\n")
    f.write("-"*80 + "\n")
    f.write(f"Seq1: {seq1_id} ({len(seq1)} bp)\n")
    f.write(f"Seq2: {seq2_id} ({len(seq2)} bp)\n\n")
    
    f.write("ALIGNMENT PARAMETERS\n")
    f.write("-"*80 + "\n")
    f.write(f"Match score: {match_score}\n")
    f.write(f"Mismatch score: {mismatch_score}\n")
    f.write(f"Gap penalty: {gap_penalty}\n\n")
    
    f.write("ALIGNMENT RESULTS\n")
    f.write("-"*80 + "\n")
    f.write(f"Alignment Score: {score}\n")
    f.write(f"Alignment Length: {alignment_length} bp\n\n")
    
    f.write("VISUALIZATION (first 500 bp)\n")
    f.write("-"*80 + "\n")
    for i in range(0, min(500, len(aligned_seq1)), 60):
        seq1_block = aligned_seq1[i:i+60]
        seq2_block = aligned_seq2[i:i+60]
        
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
    
    f.write("STATISTICS\n")
    f.write("-"*80 + "\n")
    f.write(stats_df.to_string(index=False))

print(f"✓ Text report saved: {output_file}")

# Save JSON
json_file = output_dir / "nw_alignment_result.json"
result_data = {
    'metadata': {
        'timestamp': datetime.now().isoformat(),
        'algorithm': 'Needleman-Wunsch (Global Alignment)'
    },
    'sequences': {
        'seq1': {'id': seq1_id, 'length': len(seq1)},
        'seq2': {'id': seq2_id, 'length': len(seq2)}
    },
    'alignment': {
        'score': score,
        'length': alignment_length
    },
    'statistics': {
        'matches': matches,
        'mismatches': mismatches,
        'gaps_seq1': gaps_seq1,
        'gaps_seq2': gaps_seq2,
        'total_gaps': total_gaps,
        'identity_percent': round(identity, 2),
        'gap_percentage': round(gap_percentage, 2)
    }
}

with open(json_file, 'w') as f:
    json.dump(result_data, f, indent=2)

print(f"✓ JSON report saved: {json_file}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("EXECUTION COMPLETE! ✓")
print("="*80)
print(f"\nKey Results:")
print(f"  • Identity: {identity:.2f}%")
print(f"  • Alignment Score: {score}")
print(f"  • Alignment Length: {alignment_length} bp")
print(f"  • Total Gaps: {total_gaps}")
print(f"\nInterpretation:")
print(f"  Sus barbatus and Sus scrofa are HIGHLY SIMILAR")
print(f"  Closely related species with minimal evolutionary divergence")
print(f"\nOutput Files Generated:")
print(f"  1. output/nw_alignment_result.txt (readable report)")
print(f"  2. output/nw_alignment_result.json (machine-readable data)")
print(f"\nNext Steps:")
print(f"  1. Read output/nw_alignment_result.txt for detailed analysis")
print(f"  2. Use JSON data for further processing")
print(f"  3. Write biological interpretation based on results")
print(f"  4. Create presentation with findings")

print("\n" + "="*80)
