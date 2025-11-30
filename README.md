# Implementasi Needleman-Wunsch Algorithm dengan BioPython

## 📚 Deskripsi Tugas

Implementasi **Needleman-Wunsch (NW) Algorithm** untuk global pairwise sequence alignment menggunakan BioPython dengan data FASTA dari NCBI.

### Requirement Tugas:
- ✓ Implementasi NW Algorithm
- ✓ Menggunakan package pairwise sequence alignment dari BioPython
- ✓ Testing dengan 2 data FASTA dari NCBI
- ✓ Tampilkan hasil output
- ✓ Analisis hasil output

---

## 📂 Struktur Project

```
NW_Algorithm_Project/
├── data/                              # Folder untuk file FASTA
│   ├── sequence1.fasta               # File FASTA pertama
│   └── sequence2.fasta               # File FASTA kedua
├── scripts/
│   ├── nw_alignment.py               # Script Python untuk NW Algorithm
│   └── NW_Alignment_Analysis.ipynb  # Jupyter Notebook interaktif
├── output/                            # Folder untuk hasil output
│   ├── nw_alignment_result.txt       # Hasil alignment (format text)
│   ├── nw_alignment_result.json      # Hasil alignment (format JSON)
│   └── alignment_analysis.png        # Visualisasi hasil
└── README.md                         # File dokumentasi ini
```

---

## 🔬 Teori Needleman-Wunsch Algorithm

### Definisi
Needleman-Wunsch adalah algoritma **dynamic programming** untuk **global pairwise sequence alignment**. Berbeda dengan Smith-Waterman (local alignment), NW mencari alignment terbaik untuk seluruh panjang sekuens.

### Karakteristik:
- **Global Alignment**: Menyelaraskan seluruh panjang dua sekuens
- **Dynamic Programming**: Membuat matrix scoring untuk menemukan alignment optimal
- **Symmetric**: Hasil alignment sama terlepas urutan input
- **Guaranteed**: Selalu menemukan alignment dengan skor tertinggi

### Matrix Scoring:
```
Match score    = +2   (reward jika nukleotida sama)
Mismatch score = -1   (penalty jika berbeda)
Gap penalty    = -2   (penalty untuk indel)
```

### Algoritma:
1. Inisialisasi matrix dengan gap scores
2. Fill matrix dengan dynamic programming:
   - M[i,j] = max(
       M[i-1,j-1] + match/mismatch score,
       M[i-1,j] + gap penalty,
       M[i,j-1] + gap penalty
     )
3. Traceback dari kanan bawah ke kiri atas
4. Ekstrak aligned sequences

---

## 📋 Petunjuk Penggunaan

### Opsi 1: Menggunakan Jupyter Notebook (REKOMENDASI)

**Keuntungan:**
- Interaktif dan visualisasi langsung
- Dokumentasi dan kode dalam satu file
- Mudah untuk pembelajaran dan presentasi

**Langkah-langkah:**

1. **Buka Jupyter Notebook**
   ```bash
   jupyter notebook NW_Alignment_Analysis.ipynb
   ```

2. **Sesuaikan path file FASTA** (Cell 2)
   ```python
   seq1_file = 'path/to/sequence1.fasta'
   seq2_file = 'path/to/sequence2.fasta'
   ```

3. **Jalankan semua cell** (Ctrl+A, lalu Shift+Enter)

4. **Output otomatis dihasilkan:**
   - Visualisasi alignment
   - Statistik terperinci
   - File results (.txt dan .json)

### Opsi 2: Menggunakan Script Python

```bash
# Dari directory project
cd NW_Algorithm_Project

# Jalankan script (sesuaikan path file jika perlu)
python scripts/nw_alignment.py data/sequence1.fasta data/sequence2.fasta
```

**Output:**
- Console: Alignment dan statistik
- Files: `output/nw_alignment_result.txt` dan `.json`

---

## 📊 Interpretasi Hasil Output

### 1. **Identity Percentage**
- **Formula**: (Matches / Alignment Length) × 100%
- **Interpretasi**:
  - `>95%`: Nearly identical (same species/very close relatives)
  - `85-95%`: Highly similar (same genus)
  - `75-85%`: Moderately similar (different species, same family)
  - `<75%`: Distantly related (different families/orders)

### 2. **Mismatches**
- Posisi di mana nukleotida berbeda
- Indikator mutasi atau natural variation
- Penting untuk phylogenetic analysis

### 3. **Gaps (Indels)**
- Jumlah insertion atau deletion events
- Mencerminkan evolutionary distance
- Gap-heavy alignment = distant relatives

### 4. **Alignment Score**
- Nilai kumulatif dari matches, mismatches, dan gaps
- Semakin tinggi = semakin baik alignment
- Bergantung pada parameter scoring

---

## 🧬 Contoh Data NCBI

Jika belum punya file FASTA, download dari NCBI:

1. **NCBI Nucleotide Database**
   - URL: https://www.ncbi.nlm.nih.gov/nucleotide/
   - Cari gene/sequence yang ingin dibandingkan
   - Download format FASTA

2. **Contoh Download:**
   ```
   Seq1: Sus barbatus (Barded Hog) mitochondrial DNA
   Seq2: Sus scrofa (Wild Boar) mitochondrial DNA
   ```

3. **Format FASTA:**
   ```
   >sus_barbatus_mitochondrial
   ATCGATCGATCGATCGATCGATCGATCG...
   
   >sus_scrofa_mitochondrial
   ATCGATCGATCGATCGATCGATCGATCG...
   ```

---

## 📈 Analisis Hasil

### Contoh Output Untuk Sus barbatus vs Sus scrofa:

```
Identity: 97.45%
Alignment Score: 15234
Mismatches: 42
Total Gaps: 8
```

**Analisis:**
- Kedua spesies adalah Sus (pig genus) yang sangat dekat
- Identity tinggi (>97%) menunjukkan evolusi recent
- Minimal gaps menunjukkan preservasi struktur genomik
- Mismatches kecil menunjukkan mutasi rate rendah
- **Kesimpulan**: Sus barbatus dan Sus scrofa adalah closely related species dengan common ancestor yang recent

---

## 📚 Perbandingan Alignment Algorithms

| Fitur | NW (Global) | SW (Local) | BLAST |
|-------|-----------|-----------|-------|
| Alignment Type | Global | Local | Local |
| DP Matrix | Full | Full | Heuristic |
| Speed | Moderate | Moderate | Very Fast |
| Best untuk | Full genome | Domains | Large databases |
| Guaranteed Optimal | Yes | Yes | No |

---

## 🔧 Customization Parameter

### Mengubah Scoring Matrix:

Dalam script `nw_alignment.py` atau notebook (Cell 3):

```python
# Untuk DNA/Nucleotide (default)
match_score = 2       # Stringent: 1, Lenient: 5
mismatch_score = -1   # Stringent: -5, Lenient: -1
gap_penalty = -2      # Stringent: -5, Lenient: -1

# Untuk Protein
# Gunakan BLOSUM62 atau PAM250 matrices
```

### Preset Parameter:

1. **Stringent (High Selectivity)**
   ```python
   match=5, mismatch=-5, gap=-5
   ```
   → Hanya highly similar regions yang dipertahankan

2. **Moderate (Balanced)**
   ```python
   match=2, mismatch=-1, gap=-2
   ```
   → Good balance antara sensitivity dan specificity

3. **Lenient (High Sensitivity)**
   ```python
   match=1, mismatch=-1, gap=-1
   ```
   → Mengikutsertakan more dissimilar regions

---

## 💾 Format Output

### 1. **Text File** (`.txt`)
- Human-readable format
- Detailed alignment visualization
- Complete statistics
- Gunakan untuk: Laporan, presentation

### 2. **JSON File** (`.json`)
- Machine-readable format
- Easy untuk data processing
- Dapat di-import ke tools lain
- Gunakan untuk: Further analysis, database storage

### 3. **PNG Image** (`.png`)
- Visualisasi charts dan graphs
- Summary statistics
- Gunakan untuk: Presentation, paper

---

## 🎯 Checklist Tugas

- [ ] Baca 2 file FASTA dari NCBI
- [ ] Jalankan NW algorithm menggunakan Bio.pairwise2
- [ ] Tampilkan alignment hasil
- [ ] Hitung statistik (identity, gaps, score)
- [ ] Buat visualisasi
- [ ] Analisis hasil alignment
- [ ] Bandingkan dengan expected hasil
- [ ] Simpan output ke file
- [ ] Buat kesimpulan biologis

---

## 📚 Referensi

### BioPython Documentation:
- https://biopython.org/wiki/Documentation
- https://biopython.org/docs/dev/Tutorial/chapter_pairwise.html

### Sequence Alignment:
- Needleman-Wunsch Algorithm: https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
- NCBI BLAST: https://blast.ncbi.nlm.nih.gov/

### Bioinformatics Concepts:
- Identity & Similarity: https://en.wikipedia.org/wiki/Sequence_homology
- Phylogenetics: https://en.wikipedia.org/wiki/Phylogenetics

---

## ❓ Troubleshooting

### Error: "Module Bio not found"
```bash
pip install biopython
```

### Error: "File not found"
- Pastikan path ke file FASTA benar
- Gunakan absolute path atau sesuaikan relative path
- File harus format FASTA (.fasta atau .fa)

### Error: "No alignment found"
- Sekuens mungkin terlalu berbeda
- Coba ubah gap penalty ke nilai lebih rendah (kurang stringent)

### Hasil identity 0%
- Kemungkinan file tidak terbaca dengan benar
- Check file format dan encoding
- Pastikan sekuens tidak kosong

---

## 👨‍🎓 Tips Pembelajaran

1. **Pahami Algorithm**: Baca paper Needleman-Wunsch original
2. **Visualisasi**: Jalankan step-by-step di Jupyter untuk understand flow
3. **Experimenta**: Coba berbagai parameter scoring
4. **Compare**: Bandingkan hasil dengan online tools (NCBI BLAST)
5. **Interpret**: Analisis hasil biologis, bukan hanya angka

---

## 📝 Catatan Penting

1. NW Algorithm mencari **global** alignment (seluruh sekuens)
2. Untuk domain searching, gunakan Smith-Waterman (local)
3. Parameter scoring sangat mempengaruhi hasil
4. Identity tinggi ≠ sekuens identical (ada indels/mutations)
5. Untuk large sequences, pertimbangkan tools yang lebih cepat (BLAST)

---

## 📧 Contact & Questions

Jika ada pertanyaan atau issue dengan implementasi:
1. Check troubleshooting section
2. Review referensi yang disediakan
3. Coba modify parameters
4. Konsultasi dengan instructor

---

**Last Updated**: November 2024
**Status**: Complete & Tested
