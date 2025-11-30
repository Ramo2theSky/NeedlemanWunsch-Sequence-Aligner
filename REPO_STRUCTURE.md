# Repository Structure - NeedlemanWunsch-Sequence-Aligner

```
NeedlemanWunsch-Sequence-Aligner/
│
├── README.md                          # Main documentation
├── LICENSE                            # MIT License
├── setup.py                           # Package configuration
├── pyproject.toml                     # Python project metadata
├── requirements.txt                   # Dependencies
├── .gitignore                         # Git ignore rules
│
├── nw_alignment/                      # MAIN PYTHON PACKAGE
│   ├── __init__.py                   # Package initialization
│   ├── alignment.py                  # NW algorithm implementation (Core)
│   ├── parser.py                     # FASTA file parsing
│   ├── visualization.py              # Matplotlib visualizations
│   ├── utils.py                      # Helper functions
│   └── __pycache__/                  # Python cache
│
├── scripts/                           # EXECUTABLE SCRIPTS
│   ├── run_nw_algorithm.py           # MAIN SCRIPT (Recommended for full files)
│   ├── batch_analysis.py             # Batch processing multiple files
│   ├── nw_analysis_notebook.ipynb    # Jupyter notebook version
│   └── __pycache__/
│
├── notebooks/                         # JUPYTER NOTEBOOKS
│   └── tutorial.ipynb                # Interactive tutorial
│
├── data/                              # INPUT DATA
│   ├── sequence1.fasta               # Sus barbatus mitochondrial DNA
│   └── sequence2.fasta               # Sus scrofa mitochondrial DNA
│
├── output/                            # OUTPUT RESULTS
│   ├── alignment.json                # Structured results
│   ├── alignment.txt                 # Text report
│   ├── alignment_statistics.png      # Pie chart
│   ├── alignment_percentage.png      # Distribution
│   ├── alignment_gap_analysis.png    # Gap visualization
│   └── (+ other visualization files)
│
├── examples/                          # EXAMPLE OUTPUT
│   ├── alignment.json
│   ├── alignment.txt
│   ├── alignment_statistics.png
│   └── alignment_comprehensive_overview.png
│
├── docs/                              # DOCUMENTATION
│   ├── INSTALLATION.md               # Setup instructions
│   ├── USAGE.md                      # How to use (Python vs Notebook)
│   └── ALGORITHM_EXPLANATION.md      # Technical details
│
├── tests/                             # UNIT TESTS
│   ├── __init__.py
│   ├── test_alignment.py             # Test alignment functions
│   ├── test_parser.py                # Test FASTA parsing
│   └── __pycache__/
│
└── ALGORITHM_TUTORIAL.md              # Tutorial documentation

```

## Total Files: 44
- Python source files: 8
- Configuration files: 5
- Documentation files: 6
- Test files: 3
- Data files: 2
- Output files: 12
- Example files: 4
- Notebooks: 2

## Key Features

✓ **Professional Package Structure**
  - Pure Python package in nw_alignment/
  - Proper import hierarchy
  - Modular design

✓ **Multiple Usage Options**
  - Python script (recommended for full FASTA)
  - Jupyter notebook (for interactive learning)
  - Batch processing capability

✓ **Comprehensive Documentation**
  - Installation guide
  - Usage guide
  - Algorithm explanation
  - Interactive tutorial

✓ **Ready for Production**
  - Setup.py for installation
  - Requirements.txt for dependencies
  - Proper package metadata

✓ **Clean & Reparable**
  - All temporary files cleaned
  - Output organized in separate folders
  - Examples for reference
  - __pycache__ ignored by .gitignore
