# Needleman-Wunsch Algorithm Explanation

## Overview

The Needleman-Wunsch (NW) algorithm is a dynamic programming approach for performing global pairwise sequence alignment. It finds the optimal alignment of two entire sequences.

## Key Characteristics

- **Type**: Global Alignment (entire sequences)
- **Method**: Dynamic Programming
- **Guarantee**: Always finds the optimal solution
- **Complexity**: O(m × n) where m, n = sequence lengths
- **Use Case**: Comparing homologous sequences

## How It Works

### Step 1: Initialize Scoring Matrix

Create an (m+1) × (n+1) matrix where:
- m = length of sequence 1
- n = length of sequence 2

Initialize first row and column with gap penalties:
```
    ""  A  C  G  T
""   0 -2 -4 -6 -8
A   -2
C   -4
G   -6
T   -8
```

### Step 2: Fill Matrix (Dynamic Programming)

For each cell (i,j), calculate:

```
M[i,j] = max(
    M[i-1,j-1] + s(x[i], y[j]),    # Match/Mismatch
    M[i-1,j] + gap_penalty,        # Deletion
    M[i,j-1] + gap_penalty         # Insertion
)
```

Where:
- `s(x[i], y[j])` = match score (+2) if bases match, mismatch score (-1) if different
- `gap_penalty` = -2

Example:
```
    ""  A  C  G
""   0 -2 -4 -6
A   -2  2  0 -2
C   -4  0  4  2
G   -6 -2  2  6
```

### Step 3: Traceback

Starting from M[m,n], follow the highest-scoring path back to M[0,0]:

```
    ""  A  C  G
""   0 -2 -4 -6
A   -2  2← 0 -2
C   -4  0↖ 4← 2
G   -6 -2  2↖ 6
```

Result:
```
Seq1: ACG
Seq2: ACG
Score: 6
```

## Scoring Parameters

### Default Parameters (DNA/RNA)

```
Match:    +2   (reward identical bases)
Mismatch: -1   (penalty for different bases)
Gap:      -2   (penalty for indel)
```

### Why These Values?

- **Match (+2)**: Positive reward encourages keeping matching bases together
- **Mismatch (-1)**: Small penalty reflects mutations as evolutionary events
- **Gap (-2)**: Moderate penalty prevents excessive gaps while allowing real indels

### Effect on Results

```
STRINGENT (match=5, mismatch=-5, gap=-5):
→ Only perfect matches preferred
→ Short alignments with high identity

MODERATE (match=2, mismatch=-1, gap=-2):
→ Balance between matches and gaps
→ Long alignments with good identity
→ RECOMMENDED FOR MOST CASES

LENIENT (match=1, mismatch=-1, gap=-1):
→ All events treated similarly
→ Very long alignments but less meaningful
```

## Example: Sus barbatus vs Sus scrofa

### Input
- Sequence 1 (Sus barbatus): 16,480 bp
- Sequence 2 (Sus scrofa): 16,613 bp
- Parameters: match=2, mismatch=-1, gap=-2

### Processing
```
Matrix size: 16,481 × 16,614 = ~274 million cells computed
Time: < 5 seconds (optimized)
```

### Output
```
Alignment Score:    31410.0 (EXCELLENT)
Identity:          96.62% (NEARLY IDENTICAL)
Matches:           16055 bp
Mismatches:        422 bp
Gaps:              139 bp (0.84%)
```

### Interpretation
```
Identity 96.62% + Same Genus + Very few gaps
    ↓
VERY CLOSELY RELATED SPECIES
    ↓
Recent common ancestor (~7-10 million years ago)
```

## NW vs Smith-Waterman

| Aspect | NW | SW |
|--------|----|----|
| **Alignment Type** | Global | Local |
| **Coverage** | Entire sequences | High-scoring regions |
| **Use Case** | Full sequence comparison | Domain/motif finding |
| **Example Use** | Orthologous genes | Functional domains |

**When to use NW:**
- Comparing full-length genes
- Ortholog identification
- Phylogenetic analysis

**When to use SW:**
- Finding conserved domains
- Motif discovery
- Local sequence similarity

## Complexity Analysis

| Aspect | Complexity |
|--------|-----------|
| **Time** | O(m × n) |
| **Space** | O(m × n) |

For our example:
- m = 16,480 bp
- n = 16,613 bp
- Total operations: ~274 million
- Memory: ~1-2 GB (standard matrix)
- Time: < 5 seconds (optimized code)

## Why This Implementation

This project uses **BioPython's optimized implementation** (`Bio.pairwise2.align.globalms`) which:

1. **Efficient**: Uses C-level optimization
2. **Reliable**: Battle-tested in production
3. **Flexible**: Supports custom scoring matrices
4. **Well-documented**: Part of established library

---

## References

1. Needleman, S.B. and Wunsch, C.D. (1970). A general method applicable to the search for similarities in the amino acid sequence of two proteins. *Journal of Molecular Biology*, 48(3), 443-453.

2. BioPython Tutorial: https://biopython.org/wiki/Documentation

3. NCBI BLAST Scoring: https://www.ncbi.nlm.nih.gov/books/NBK62051/
