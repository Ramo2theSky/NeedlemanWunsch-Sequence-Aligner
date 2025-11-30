#!/usr/bin/env python
"""
Setup script for nw-algorithm-biopython package
"""

from setuptools import setup, find_packages

setup(
    name="nw-algorithm-biopython",
    version="1.0.0",
    description="Needleman-Wunsch Algorithm Implementation for Sequence Alignment",
    author="Ramo2theSky",
    author_email="your.email@example.com",
    url="https://github.com/Ramo2theSky/NeedlemanWunsch-Sequence-Aligner",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "biopython>=1.81",
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.12',
        ],
        'docs': [
            'sphinx>=4.0',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="bioinformatics sequence-alignment needleman-wunsch pairwise-alignment dna-sequence",
    entry_points={
        'console_scripts': [
            'nw-align=scripts.run_nw_algorithm:main',
        ],
    },
)
