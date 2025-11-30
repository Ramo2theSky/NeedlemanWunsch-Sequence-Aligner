# 🧬 NEEDLEMAN-WUNSCH ALGORITHM TUTORIAL

## Pengenalan Algoritma

### Definisi Sederhana
Needleman-Wunsch adalah cara **smart** untuk menyelaraskan dua sekuens DNA/Protein sehingga kita bisa:
- Melihat kesamaan mereka
- Menemukan pola evolusi
- Mengidentifikasi mutations

### Karakteristik Utama
- ✅ **Global Alignment** = menyelaraskan SELURUH sekuens
- ✅ **Optimal Solution** = SELALU menemukan alignment terbaik
- ✅ **Dynamic Programming** = menggunakan matrix scoring
- ✅ **Symmetric** = hasil sama untuk input apapun urutan

---

## Cara Kerja (Step-by-Step)

### Step 1: Siapkan Data
```
Seq1: ATCG
Seq2: ACG

Panjang: 4 dan 3
```

### Step 2: Buat Scoring Matrix
```
        ""  A  C  G
    ""   0 -2 -4 -6
    A   -2  2 -1 -3
    T   -4 -1 -1 -2
    C   -6  0  1 -2
    G   -8 -2  0  2

Penjelasan:
- Match (A-A, T-T, etc) = +2
- Mismatch = -1
- Gap = -2
```

### Step 3: Fill Matrix (Dynamic Programming)
```
Untuk setiap cell [i,j]:
  M[i,j] = max(
    M[i-1,j-1] + score(seq1[i], seq2[j]),  # diagonal
    M[i-1,j] + gap_penalty,                 # vertical (gap di seq2)
    M[i,j-1] + gap_penalty                  # horizontal (gap di seq1)
  )

Pilih nilai terbesar!
```

### Step 4: Traceback (Ambil Alignment)
```
Dari kanan bawah ke kiri atas, ambil path dengan skor tertinggi

Hasil akhir:
ATCG
A-CG

Score = 4 (2+(-2)+2+2)
```

---

## Contoh Konkret

### Data Input
```
Seq1: GAATTCAGTTA (panjang 11)
Seq2: GGATCGA     (panjang 7)

Tujuan: Cari alignment terbaik!
```

### Expected Alignment
```
GAATTCAGTTA
G-A--TC-A--
GGATC-GA---

Matches: G, A, T, C, A (= 5 position)
Mismatches: 0 position (tidak ada nukleotida beda di posisi align)
Gaps: Banyak

Identity = 5/11 = 45%
```

---

## Interpretasi Score

### Score Formula
```
Score = (Matches × match_score) 
        + (Mismatches × mismatch_score)
        + (Gaps × gap_penalty)

Contoh:
5 matches × (+2) = +10
0 mismatches × (-1) = 0
6 gaps × (-2) = -12
Total Score = 10 + 0 - 12 = -2
```

### Skor Tinggi = Alignment Baik ✅
```
Score = 100    = SANGAT MIRIP (>95% identity)
Score = 50     = MIRIP (85-95% identity)
Score = 0      = CUKUP MIRIP (75-85% identity)
Score = -10    = BERBEDA (<75% identity)
```

---

## Parameter Scoring: Pengaruhnya

### Parameter 1: Match Score
```
Match = +2 (DEFAULT)   → Rewards similarity, lebih ketat
Match = +5 (STRINGENT) → Sangat rewards, hanya match bagus
Match = +1 (LENIENT)   → Minimal reward, lebih permissive
```

### Parameter 2: Mismatch Penalty
```
Mismatch = -1 (DEFAULT)   → Small penalty untuk divergence
Mismatch = -5 (STRINGENT) → Heavy penalty, avoid divergence
Mismatch = -1 (LENIENT)   → Minimal penalty
```

### Parameter 3: Gap Penalty
```
Gap = -2 (DEFAULT)   → Moderate cost untuk indel
Gap = -5 (STRINGENT) → Heavy cost, avoid gaps
Gap = -1 (LENIENT)   → Low cost, allow many gaps
```

### Pengaruh Kombinasi
```
STRINGENT (match=5, mismatch=-5, gap=-5):
→ Hanya perfectly matching regions
→ Hasil: Alignment pendek, tapi sangat mirip

MODERATE (match=2, mismatch=-1, gap=-2):
→ Balance antara match dan gaps
→ Hasil: Alignment panjang, cukup mirip
→ RECOMMENDED!

LENIENT (match=1, mismatch=-1, gap=-1):
→ Hampir semua diberi skor sama
→ Hasil: Alignment panjang, tapi kurang meaningful
```

---

## Aplikasi Biologis

### 1. Sequence Comparison
```
Seq dari organism berbeda → Cari homologi
Identity tinggi → Evolusi recent
Identity rendah → Divergence lama
```

### 2. Mutation Detection
```
Mismatch di alignment → Mutasi yang terjadi
Gap = Insertion/Deletion event
Banyak gap = Struktur berbeda
```

### 3. Phylogenetic Analysis
```
Identity score → Evolutionary distance
Identity 95% → Sister species
Identity 80% → Sama family
Identity 50% → Beda order
```

### 4. Gene Annotation
```
Align unknown sequence vs database
Tinggi identity → Sama gene
Rendah identity → Beda gene atau ortho
```

---

## Perbedaan NW vs Smith-Waterman

| Aspek | Needleman-Wunsch (NW) | Smith-Waterman (SW) |
|-------|----------------------|-------------------|
| Alignment Type | **GLOBAL** (full length) | **LOCAL** (sub-regions) |
| Use Case | Compare full genes | Find domains/motifs |
| Better for | Homologous sequences | Diverged sequences |
| Example | Comparing orthologs | Finding conserved domains |
| Speed | Moderate | Moderate |

```
Contoh:
NW: ATCGATCGATCGATCGATCG
    ||||||||||||||||||||  (seluruh aligned)
    ATCGATCGATCGATCGATCG

SW: ATCGATCGATCGATCGATCG
           ||||||||||    (hanya bagian mirip)
        ATCGATCGATCG
```

---

## Praktik: Calculate Manual Score

### Data
```
Seq1: ATG
Seq2: AGG

Match = +1, Mismatch = -1, Gap = -1
```

### Matrix
```
        ""  A  G  G
    ""   0 -1 -2 -3
    A   -1  1  0 -1
    T   -2  0  0  ?
    G   -3 -1  1  1
```

### Isi cell ?
```
Position [2,3] (T vs G):
Opsi 1: [1,2] + score(T,G) = 0 + (-1) = -1  (diagonal/mismatch)
Opsi 2: [1,3] + gap_penalty = -1 + (-1) = -2  (atas/gap di seq1)
Opsi 3: [2,2] + gap_penalty = 0 + (-1) = -1   (kiri/gap di seq2)

Max = -1 ✓

Jadi cell [2,3] = -1
```

### Hasil Traceback
```
Seq1: A-TG
Seq2: AGG-

Score = 1 + (-1) + 1 + (-1) = 0
```

---

## Tips & Tricks

### 1. Memilih Parameter
```
👉 Default (2, -1, -2) cocok untuk kebanyakan kasus
👉 DNA nucleotide: gunakan match/mismatch (tidak perlu matrix)
👉 Protein: gunakan BLOSUM62 atau PAM250
```

### 2. Interpreting Results
```
✅ Identity 95%+ = Nearly identical, minimal evolution
✅ Identity 85%  = Homologous, sama family
✅ Identity 75%  = Related, sama superfamily
❌ Identity 50%  = Distant, beda order/class
```

### 3. Debugging
```
❓ Score negatif? Normal! Banyak gaps/mismatches
❓ Score 0? Seq sangat berbeda
❓ Score sangat besar? Seq sangat mirip
```

### 4. Performance
```
⚡ <1000 bp: instant
⚡ 1000-10000 bp: <1 detik
⚡ 10000-100000 bp: <10 detik
⚡ >100000 bp: gunakan BLAST (heuristic, faster)
```

---

## BioPython Implementation

### Syntax Dasar
```python
from Bio import pairwise2

alignments = pairwise2.align.globalms(
    seq1, 
    seq2,
    match_score=2,           # score jika sama
    mismatch_score=-1,       # score jika beda
    gap_penalty=-2,          # penalty per gap
    gap_penalty_extension=-2 # penalty per gap extension
)

# Ambil alignment terbaik
best = alignments[0]
aligned_seq1, aligned_seq2, score, begin, end = best

# Akses hasil
print(aligned_seq1)  # sekuens 1 aligned
print(aligned_seq2)  # sekuens 2 aligned
print(score)         # skor total
```

### Variasi Fungsi
```python
# globalxx: exact match vs mismatch (SIMPLE)
pairwise2.align.globalxx(seq1, seq2)

# globalms: match/mismatch scoring (RECOMMENDED)
pairwise2.align.globalms(seq1, seq2, match, mismatch, gap, gap_ext)

# globalxs: exact match vs mismatch, with affine gap
pairwise2.align.globalxs(seq1, seq2, gap_open, gap_extend)

# globalds: exact match vs mismatch, dengan scoring matrix
pairwise2.align.globalds(seq1, seq2, matrix, gap_open, gap_extend)
```

---

## Latihan

### Exercise 1: Manual Calculation
```
Seq1: CAT
Seq2: TAC
Match=1, Mismatch=-1, Gap=-1

Buat matrix dan cari score!
Jawab: Score = ?
```

### Exercise 2: Parameter Tuning
```
Jalankan dengan 3 parameter set berbeda:
1. Stringent: (5, -5, -5)
2. Moderate: (2, -1, -2) ← DEFAULT
3. Lenient: (1, -1, -1)

Bandingkan hasilnya!
Apa perbedaan identity-nya?
```

### Exercise 3: Interpretation
```
Diberikan hasil:
Identity: 88%, Score: 245, Gaps: 12

Apa kesimpulan biologisnya?
```

---

## Reference URLs

- Needleman-Wunsch (Wiki): https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
- BioPython Docs: https://biopython.org/docs/dev/Tutorial/chapter_pairwise.html
- Sequence Alignment: https://en.wikipedia.org/wiki/Sequence_alignment
- Scoring Matrices: https://en.wikipedia.org/wiki/Substitution_matrix

---

## Kesimpulan

✅ NW Algorithm adalah cara terstandar untuk sequence alignment
✅ Selalu menemukan optimal solution (dijamin!)
✅ Parameter sangat penting untuk hasil yang meaningful
✅ Identity % adalah metrik utama untuk perbandingan
✅ Berguna untuk evolutionary analysis, mutation detection, dan homology search

**Sekarang Anda siap untuk mengimplementasikan! 🚀**
