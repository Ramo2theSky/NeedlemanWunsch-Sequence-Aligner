"""
Visualization Functions for Alignment Results

Create publication-quality plots for alignment statistics and analysis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Optional


def plot_alignment_statistics(result: Dict, output_file: Optional[str] = None,
                             title: str = "Needleman-Wunsch Alignment Analysis") -> None:
    """
    Create comprehensive alignment statistics visualization.
    
    Args:
        result (dict): Alignment result from NWAligner.align()
        output_file (str, optional): Save figure to file. If None, displays plot.
        title (str): Plot title
        
    Example:
        >>> from nw_alignment import NWAligner
        >>> aligner = NWAligner()
        >>> result = aligner.align(seq1, seq2)
        >>> plot_alignment_statistics(result, "output.png")
    """
    stats = result['alignment_stats']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    # 1. Identity Pie Chart
    ax1 = axes[0, 0]
    identity_data = [stats['matches'], stats['mismatches']]
    colors = ['#2ecc71', '#e74c3c']
    ax1.pie(identity_data, labels=['Matches', 'Mismatches'], autopct='%1.1f%%',
            colors=colors, startangle=90)
    ax1.set_title('Identity Analysis', fontweight='bold')
    
    # 2. Alignment Composition Bar Chart
    ax2 = axes[0, 1]
    categories = ['Matches', 'Mismatches', 'Gaps']
    values = [stats['matches'], stats['mismatches'], stats['gaps']]
    bars = ax2.bar(categories, values, color=['#2ecc71', '#e74c3c', '#f39c12'])
    ax2.set_ylabel('Count (bp)')
    ax2.set_title('Alignment Composition', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    # 3. Gap Distribution
    ax3 = axes[1, 0]
    gap_labels = ['Seq1 Gaps', 'Seq2 Gaps']
    gap_values = [stats['gaps_seq1'], stats['gaps_seq2']]
    ax3.bar(gap_labels, gap_values, color=['#3498db', '#9b59b6'])
    ax3.set_ylabel('Count (bp)')
    ax3.set_title('Gap Distribution', fontweight='bold')
    for i, v in enumerate(gap_values):
        ax3.text(i, v, str(v), ha='center', va='bottom', fontsize=10)
    
    # 4. Summary Statistics Table
    ax4 = axes[1, 1]
    ax4.axis('off')
    summary_text = f"""
ALIGNMENT SUMMARY

Length:           {stats['length']} bp
Identity:         {stats['identity']:.2f}%
Score:            {stats['score']:.1f}

Matches:          {stats['matches']} ({stats['match_percentage']:.2f}%)
Mismatches:       {stats['mismatches']} ({stats['mismatch_percentage']:.2f}%)
Total Gaps:       {stats['gaps']} ({stats['gap_percentage']:.2f}%)
"""
    ax4.text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
            fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path), dpi=300, bbox_inches='tight')
        print(f"[+] Figure saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()


def plot_percentage_distribution(result: Dict, output_file: Optional[str] = None) -> None:
    """
    Create percentage distribution plot.
    
    Args:
        result (dict): Alignment result
        output_file (str, optional): Save figure to file
    """
    stats = result['alignment_stats']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Match %', 'Mismatch %', 'Gap %']
    percentages = [
        stats['match_percentage'],
        stats['mismatch_percentage'],
        stats['gap_percentage']
    ]
    colors = ['#2ecc71', '#e74c3c', '#f39c12']
    
    bars = ax.barh(categories, percentages, color=colors)
    ax.set_xlabel('Percentage (%)', fontweight='bold')
    ax.set_title('Alignment Composition (Percentage)', fontweight='bold', fontsize=14)
    ax.set_xlim(0, 100)
    
    for i, (bar, val) in enumerate(zip(bars, percentages)):
        ax.text(val + 2, bar.get_y() + bar.get_height()/2, 
               f'{val:.2f}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path), dpi=300, bbox_inches='tight')
        print(f"[+] Figure saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()


def plot_gap_analysis(result: Dict, output_file: Optional[str] = None) -> None:
    """
    Create gap analysis visualization.
    
    Args:
        result (dict): Alignment result
        output_file (str, optional): Save figure to file
    """
    stats = result['alignment_stats']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gap positions pie chart
    gap_data = [stats['gaps_seq1'], stats['gaps_seq2']]
    labels = [f"Seq1 Gaps\n({stats['gaps_seq1']})", 
              f"Seq2 Gaps\n({stats['gaps_seq2']})"]
    colors = ['#3498db', '#9b59b6']
    ax1.pie(gap_data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Gap Distribution by Sequence', fontweight='bold')
    
    # Gap percentage comparison
    gap_categories = ['Match', 'Gap']
    gap_values = [stats['length'] - stats['gaps'], stats['gaps']]
    ax2.bar(gap_categories, gap_values, color=['#2ecc71', '#e74c3c'])
    ax2.set_ylabel('Position Count (bp)')
    ax2.set_title('Aligned vs Gap Positions', fontweight='bold')
    
    for i, v in enumerate(gap_values):
        ax2.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(str(output_path), dpi=300, bbox_inches='tight')
        print(f"[+] Figure saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()
