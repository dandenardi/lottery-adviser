# Quick Reference Guide

## 🚀 Common Commands

### First Time Setup

```bash
# Install dependencies
pip install -e .

# Generate sample data (for testing)
python scripts/generate_sample_data.py

# Verify installation
python scripts/verify_installation.py
```

### Running Analysis

```bash
# Run the main pipeline
python scripts/run_pipeline.py
```

### Using Your Own Data

1. Place your Excel file at: `data/raw/lottery_history.xlsx`
2. Ensure it has these columns:
   - `concurso` (integer) - Contest number
   - `data` (date) - Draw date
   - `bola_1`, `bola_2`, ..., `bola_6` (integers) - Drawn numbers

---

## 📁 Important Files

| File                                    | Purpose                   |
| --------------------------------------- | ------------------------- |
| `scripts/run_pipeline.py`               | Main CLI - run analysis   |
| `scripts/generate_sample_data.py`       | Create test data          |
| `scripts/verify_installation.py`        | Test installation         |
| `data/raw/lottery_history.xlsx`         | Your lottery data (input) |
| `data/processed/latest_statistics.json` | Analysis results (output) |

---

## 🔧 Project Structure

```
app/
├── collectors/      → Fetch lottery results (future)
├── storage/         → Read/write Excel files
├── analysis/        → Compute statistics
└── pipelines/       → Orchestrate workflow
```

---

## 📊 What Statistics Are Computed?

- **Frequency Analysis**: Which numbers appear most/least often
- **Distribution**: Even vs odd, number ranges
- **Aggregates**: Average sum of drawn numbers
- **Date Range**: First and last draw dates

---

## 🐛 Troubleshooting

### "File not found" error

```bash
# Generate sample data
python scripts/generate_sample_data.py
```

### Import errors

```bash
# Reinstall package
pip install -e .
```

### Excel format errors

Make sure your file has columns: `concurso`, `data`, `bola_1`, `bola_2`, etc.

---

## 📚 Documentation

- **README.md** - Project overview
- **SETUP.md** - Detailed installation guide
- **DEVELOPMENT.md** - Developer documentation
- **This file** - Quick reference

---

## 🔮 Future Features (Not Yet Implemented)

- ⏳ Web scraping for automatic updates
- ⏳ LLM-based pattern analysis
- ⏳ Strategy generation
- ⏳ Web dashboard
- ⏳ REST API

---

## ⚠️ Important Notes

- This system **does NOT predict** lottery results
- All analysis is purely statistical
- Use for educational purposes only
- No guarantees of accuracy or success

---

## 💡 Tips

1. **Start with sample data** to understand the system
2. **Check the JSON output** for detailed statistics
3. **Read DEVELOPMENT.md** to understand the architecture
4. **Keep your data backed up** before adding new results

---

## 🎯 Next Steps

1. ✅ Install dependencies: `pip install -e .`
2. ✅ Verify installation: `python scripts/verify_installation.py`
3. ✅ Run with sample data: `python scripts/run_pipeline.py`
4. 📝 Add your real data to `data/raw/lottery_history.xlsx`
5. 🚀 Run analysis again with your data

---

## 📞 Need Help?

Check the documentation:

- Installation issues → **SETUP.md**
- Understanding the code → **DEVELOPMENT.md**
- General info → **README.md**
