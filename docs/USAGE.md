# Usage Guide

## Quick Start

### Method 1: Using Python Script (RECOMMENDED for Full Files)

For complete FASTA file processing without RAM limitations:

```bash
cd scripts
python run_nw_algorithm.py -s1 ../data/sequence1.fasta -s2 ../data/sequence2.fasta
```

**Output files will be saved in `../output/`:**
- `alignment.txt` - Detailed alignment report
- `alignment.json` - Structured results (for analysis)
- `alignment_*.png` - Visualization charts

**Why use the script?**
- ✅ Processes FULL FASTA files (no RAM limitations)
- ✅ More efficient memory management
- ✅ Professional output formatting
- ✅ Better for large sequences

---

### Method 2: Using Jupyter Notebook (For Learning)

```bash
jupyter notebook notebooks/tutorial.ipynb
```

Run all cells to perform alignment and see visualizations.

**Limitations:**
- RAM-limited (Google Colab: ~12GB)
- Better for smaller sequences or tutorials

---

## Example Workflow

### Step 1: Prepare Your Data

Place your FASTA files in `data/` folder:
```
data/
├── sequence1.fasta
└── sequence2.fasta
```

Format example:
```fasta
>Sus_barbatus_mitochondrial_DNA
ATCGATCGATCGATCGATCGATCGATCGATCG...
```

### Step 2: Run Alignment

```bash
python scripts/run_nw_algorithm.py -s1 data/sequence1.fasta -s2 data/sequence2.fasta
```

### Step 3: Check Results

```bash
# View text report
cat output/alignment.txt

# View JSON results (for analysis in Python)
python -c "import json; data=json.load(open('output/alignment.json')); print(data['statistics'])"

# View visualizations
# Open output/alignment_statistics.png in your image viewer
```

---

## Advanced Usage

### Custom Scoring Parameters

Edit `scripts/run_nw_algorithm.py` and modify:

```python
match_score = 2       # Change to your preference
mismatch_score = -1   # Change to your preference
gap_penalty = -2      # Change to your preference
```

Then run:
```bash
python scripts/run_nw_algorithm.py -s1 data/sequence1.fasta -s2 data/sequence2.fasta
```

### Batch Processing Multiple Files

```bash
python scripts/batch_analysis.py data/
```

This processes all FASTA files in the `data/` directory.

### Compare Multiple Sequences

```bash
python scripts/compare_sequences.py -f data/sequence1.fasta data/sequence2.fasta data/sequence3.fasta
```

---

## Understanding Output

### alignment.txt
Human-readable alignment with:
- Sequence IDs and lengths
- Full pairwise alignment
- Statistics (matches, mismatches, gaps, identity %)
- Alignment score

### alignment.json
Machine-readable format containing:
```json
{
  "sequences": {
    "seq1_id": "...",
    "seq1_length": 16480
  },
  "alignment": {
    "score": 31410.0
  },
  "statistics": {
    "identity_percent": 96.62,
    "matches": 16055
  }
}
```

### alignment_*.png
Multiple visualizations:
- `alignment_statistics.png` - Overview
- `alignment_comprehensive_overview.png` - Detailed analysis
- `alignment_percentage.png` - Identity breakdown
- `alignment_gap_analysis.png` - Indel patterns

---

## Comparison: Script vs Notebook

| Feature | Script | Notebook |
|---------|--------|----------|
| **Full FASTA Support** | ✅ Yes | ⚠️ Limited by RAM |
| **Memory Efficient** | ✅ Yes | ❌ Loads entire sequence |
| **Interactive** | ❌ No | ✅ Yes |
| **Learning** | ❌ Less | ✅ Great |
| **Production Use** | ✅ Best | ❌ Not recommended |
| **Documentation** | ✓ Good | ✅ Excellent |

---

## Example Results (Sus barbatus vs Sus scrofa)

```
Alignment Statistics:
├── Score: 31410.0 (EXCELLENT)
├── Identity: 96.62% (NEARLY IDENTICAL)
├── Matches: 16055 bp
├── Mismatches: 422 bp
├── Gaps: 139 bp
└── Status: VERY CLOSELY RELATED SPECIES
```

---

**For more information:**
- See [ALGORITHM_EXPLANATION.md](ALGORITHM_EXPLANATION.md) for technical details
- See [examples/](../examples/) for sample outputs
