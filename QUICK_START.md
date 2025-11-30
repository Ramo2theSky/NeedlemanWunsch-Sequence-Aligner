# 🚀 QUICK START GUIDE

## Step 1: Setup Environment

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Verifikasi BioPython
```bash
python -c "import Bio; print(Bio.__version__)"
```

---

## Step 2: Jalankan Analysis

### Opsi A: Jupyter Notebook (RECOMMENDED)
```bash
# Start Jupyter
jupyter notebook

# Open: NW_Alignment_Analysis.ipynb
# Run semua cell (Ctrl+A, lalu Shift+Enter)
```

### Opsi B: Python Script
```bash
# Dari directory project
python scripts/nw_alignment.py
```

---

## Step 3: Cek Hasil Output

Output akan tersimpan di folder `output/`:
- `nw_alignment_result.txt` - Alignment detail
- `nw_alignment_result.json` - Data dalam format JSON
- `alignment_analysis.png` - Visualisasi charts

---

## 📊 Expected Output

Untuk Sus barbatus vs Sus scrofa, hasil yang diharapkan:

```
✓ Alignment Score: ~15000+
✓ Identity: ~97-98%
✓ Gaps: Sangat sedikit (<1%)
✓ Alignment Length: Full length (sudah tersedia)
```

**Interpretasi**: Kedua spesies pig yang sangat closely related!

---

## 🔍 Cara Membaca Output

### Alignment Visualization:
```
Seq1: ATCGATCGATCG...
      ||||||||||||    (| = match, . = mismatch, space = gap)
Seq2: ATCGATCGATCG...
```

### Statistics:
- **Identity**: % nukleotida yang sama
- **Matches**: Jumlah kesamaan
- **Gaps**: Insertion/deletion events
- **Score**: Kualitas overall alignment

---

## 💡 Troubleshooting

### "Module Bio not found"
```bash
pip install biopython
```

### Path error
Edit path di cell 2 notebook atau script parameter

### Visualisasi tidak tampil
```bash
pip install matplotlib seaborn
```

---

## 📚 Next Steps

1. ✅ Pahami algoritma NW (baca referensi)
2. ✅ Jalankan dengan data default
3. ✅ Modifikasi parameters (match score, gap penalty)
4. ✅ Bandingkan dengan online tools
5. ✅ Buatkan laporan analisis biologis

---

## 🎓 Learning Path

```
Minggu 1: Understanding NW Algorithm
  → Baca paper + visualisasi
  
Minggu 2: Implementation with BioPython
  → Run code + modify parameters
  
Minggu 3: Analysis & Interpretation
  → Analyze results + biological meaning
  
Minggu 4: Advanced Topics
  → Multiple alignment + phylogenetics
```

---

## ❓ Common Questions

**Q: Perbedaan NW vs Smith-Waterman?**
A: NW = global (full length), SW = local (domains only)

**Q: Kenapa hasil berubah dengan parameter berbeda?**
A: Parameter scoring mengontrol sensitivity/specificity

**Q: Bisakah align protein sequences?**
A: Ya! Gunakan BLOSUM62 matrix, sudah support.

**Q: Berapa panjang maksimal sekuens?**
A: Tergantung RAM, ~100KB biasanya OK, lebih besar gunakan BLAST.

---

## 📈 Checklist Before Submission

- [ ] File FASTA ter-copy ke data/
- [ ] Notebook/Script bisa dijalankan tanpa error
- [ ] Output files tersimpan di output/
- [ ] Baca dan pahami hasil alignment
- [ ] Tulis analisis biologis
- [ ] Include visualisasi di laporan
- [ ] Bandingkan dengan expected hasil
- [ ] Siapkan penjelasan untuk presentasi

---

**Ready to start? Let's go! 🧬**
