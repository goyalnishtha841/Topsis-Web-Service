# TOPSIS Decision Support System

A complete implementation of **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** developed as a multi-interface software system.

This project demonstrates how a decision-making algorithm can be transformed into:

- Command Line Application (CLI)
- Installable Python Package (PyPI)
- Web-based Decision Service (Flask)

## Project Overview

TOPSIS is a **Multi-Criteria Decision Making (MCDM)** technique used to rank alternatives based on multiple evaluation criteria.

The best alternative is the one:

- Closest to the **Ideal Best Solution**
- Farthest from the **Ideal Worst Solution**

This system allows users to upload datasets, define criterion importance, and automatically obtain ranked results.

## Features

- Command-line TOPSIS execution
- Input validation and error handling
- CSV and Excel file support
- Automated ranking computation
- Web interface for non-technical users
- Email delivery of results using SMTP
- Modular and reusable architecture

## Algorithm Steps (TOPSIS)

1. Normalize decision matrix
2. Apply weights to criteria
3. Determine ideal best and worst solutions
4. Compute separation distances
5. Calculate TOPSIS score
6. Rank alternatives

## Input File Format

The input file must contain:

- First column → Alternative names (non-numeric)
- Remaining columns → Numeric criteria values

## Input Validation Rules

- Minimum 3 columns required
- First column must be non-numeric
- Remaining columns must be numeric
- Number of weights = number of impacts
- Impacts must be `+` or `-`

### Example (`data.csv`)

| Fund | P1 | P2 | P3 | P4 |
|------|----|----|----|----|
| M1 | 0.67 | 0.45 | 6.5 | 42.6 |
| M2 | 0.60 | 0.36 | 3.6 | 53.3 |
| M3 | 0.82 | 0.67 | 3.8 | 63.1 |

## Weights

Weights represent the **importance** of each criterion.

### Example 
"1,1,1,2"

Meaning:
- Criterion 4 is twice as important

## Impacts

Impacts indicate whether higher values are beneficial or costly.

| Symbol | Meaning |
|--------|---------|
| + | Benefit criterion (higher is better) |
| - | Cost criterion (lower is better) |

### Example:
"+,+,-,+"

## Output

### The output file is saved as a CSV containing two additional columns:

Topsis Score – Relative performance score
Rank – Ranking of alternatives (1 = best)

## Web Service Usage

### Webservice Live Link- 
https://topsis-web-service-a9br.onrender.com

### User Workflow

1. Upload dataset
2. Enter weights
3. Enter impacts
4. Provide email address
5. Submit form
6. Receive ranked result via email

## Email System (SMTP)

The system uses Gmail SMTP server.

Authentication is performed using a **Gmail App Password**.

## PyPI Package Installation

pip install Topsis-Nishtha-102317136

## Command Line Usage

After installation, run:

topsis <InputFile> <Weights> <Impacts> <OutputFile>

### Example
topsis data.csv "1,1,1,2" "+,+,-,+" result.csv

## Author

Nishtha Goyal












