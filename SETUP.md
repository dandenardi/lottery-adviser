# Lottery Adviser - Setup Guide

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## 🚀 Installation

### 1. Clone or navigate to the repository

```bash
cd c:\programming\lottery-adviser
```

### 2. Create a virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e .
```

This will install:

- pandas (for data manipulation)
- openpyxl (for Excel file handling)
- requests (for future scraping functionality)

## 📊 Preparing Your Data

### Option 1: Use Sample Data (for testing)

Generate sample lottery data:

```bash
python scripts/generate_sample_data.py
```

This creates a file `data/raw/lottery_history.xlsx` with 100 sample lottery contests.

### Option 2: Use Real Data

Place your actual lottery history Excel file in `data/raw/lottery_history.xlsx`.

**Expected format:**

- Column `concurso`: Contest number (integer)
- Column `data`: Draw date (date format)
- Columns `bola_1`, `bola_2`, ..., `bola_6`: Drawn numbers (integers)

Example:

| concurso | data       | bola_1 | bola_2 | bola_3 | bola_4 | bola_5 | bola_6 |
| -------- | ---------- | ------ | ------ | ------ | ------ | ------ | ------ |
| 1        | 2020-01-04 | 5      | 12     | 23     | 34     | 45     | 56     |
| 2        | 2020-01-07 | 3      | 15     | 27     | 38     | 42     | 59     |

## 🎯 Running the Analysis

Execute the main pipeline:

```bash
python scripts/run_pipeline.py
```

This will:

1. Load the historical lottery data
2. Compute comprehensive statistics
3. Display results in the console
4. Save detailed statistics to `data/processed/latest_statistics.json`

## 📈 Understanding the Output

The pipeline generates the following statistics:

### Basic Information

- **Total Contests**: Number of lottery draws analyzed
- **Date Range**: First and last draw dates
- **Total Numbers**: Total count of numbers analyzed

### Frequency Analysis

- **Most Common Numbers**: Top 10 numbers that appear most frequently
- **Least Common Numbers**: Bottom 10 numbers that appear least frequently
- **Number Frequencies**: Complete frequency count for all numbers

### Distribution Analysis

- **Even/Odd Distribution**: Percentage of even vs odd numbers
- **Number Range Distribution**: How numbers are distributed across ranges (1-15, 16-30, 31-45, 46-60)

### Aggregates

- **Average Sum**: Average sum of all drawn numbers per contest

## 🏗️ Project Structure

```
lottery-adviser/
├─ app/                          # Main application package
│  ├─ collectors/                # Data collection modules
│  │  └─ lottery_collector.py   # (Future) Scraping logic
│  ├─ storage/                   # Data persistence
│  │  └─ history_repository.py  # Excel file management
│  ├─ analysis/                  # Statistical analysis
│  │  └─ statistics_service.py  # Statistics computation
│  ├─ pipelines/                 # Orchestration
│  │  └─ update_and_analyze.py  # Main pipeline
│  └─ config.py                  # Configuration settings
├─ scripts/                      # Executable scripts
│  ├─ run_pipeline.py           # Main CLI entrypoint
│  └─ generate_sample_data.py   # Sample data generator
├─ data/                         # Data directory
│  ├─ raw/                       # Raw data (tracked in git)
│  └─ processed/                 # Generated files (gitignored)
└─ pyproject.toml               # Project metadata & dependencies
```

## 🔧 Development

### Code Style

The project uses:

- **Black** for code formatting
- **Ruff** for linting

Install dev dependencies:

```bash
pip install -e ".[dev]"
```

Format code:

```bash
black app/ scripts/
```

Lint code:

```bash
ruff check app/ scripts/
```

## 🔮 Future Enhancements

The following features are planned for future milestones:

1. **Lottery Scraping**: Implement `LotteryCollector.fetch_latest_result()` to automatically fetch new results
2. **LLM Integration**: Add AI-powered pattern interpretation
3. **Strategy Generation**: Generate number selection strategies based on analysis
4. **Simulations**: Run Monte Carlo simulations to evaluate strategies
5. **Web Dashboard**: Create a web interface for visualization
6. **API**: Expose functionality via REST API

## ❓ Troubleshooting

### "File not found" error

Make sure you have a `lottery_history.xlsx` file in `data/raw/`. Run the sample data generator if needed:

```bash
python scripts/generate_sample_data.py
```

### Import errors

Ensure you've installed the package:

```bash
pip install -e .
```

### Excel file format errors

Verify your Excel file has the required columns:

- `concurso` (integer)
- `data` (date)
- `bola_1`, `bola_2`, etc. (integers)

## 📝 Notes

- This system **does not predict lottery results**
- All analysis is purely statistical and historical
- Use responsibly for educational purposes only
