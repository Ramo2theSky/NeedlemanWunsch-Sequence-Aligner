# Installation Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Step 1: Clone Repository

```bash
git clone https://github.com/Ramo2theSky/NeedlemanWunsch-Sequence-Aligner.git
cd NeedlemanWunsch-Sequence-Aligner
```

## Step 2: Install Dependencies

### Option A: Using requirements.txt (Recommended)
```bash
pip install -r requirements.txt
```

### Option B: Manual Installation
```bash
pip install biopython==1.81
pip install numpy>=1.21.0
pip install pandas>=1.3.0
pip install matplotlib>=3.4.0
pip install seaborn>=0.11.0
```

## Step 3: Verify Installation

```bash
python -c "import Bio; print(f'BioPython {Bio.__version__} installed')"
```

Expected output:
```
BioPython 1.81 installed
```

## Step 4: (Optional) Install Package Locally

For development, install the package in editable mode:

```bash
pip install -e .
```

This allows you to import the `nw_alignment` package directly:

```python
from nw_alignment.alignment import NWAlignment
```

## Troubleshooting

### Issue: "No module named 'Bio'"
**Solution:**
```bash
pip install --upgrade biopython
```

### Issue: Module import errors
**Solution:** Make sure you're in the correct directory:
```bash
cd NeedlemanWunsch-Sequence-Aligner
python scripts/run_nw_algorithm.py
```

### Issue: Out of memory
**Solution:** For very large sequences (>100MB), use the streaming version or process in chunks.

---

**Next Steps:**
- See [USAGE.md](USAGE.md) for how to run the alignment
- See [tutorial.ipynb](../notebooks/tutorial.ipynb) for interactive examples
