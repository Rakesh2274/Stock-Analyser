# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install pandas requests

# Navigate to project directory
cd /path/to/stock-analyser
```

## Run the Pipeline

```bash
# Run everything in sequence
python3 main.py
```

## What Gets Generated

After running, you'll get 4 CSV files in `data/output/`:

1. **weekly_comparison.csv** - Shows which NIFTY 50 stocks have strong delivery patterns week-over-week
2. **weekly_industry_comparison.csv** - Industry summary of the same data
3. **monthly_comparison.csv** - Same analysis but month-over-month
4. **monthly_industry_comparison.csv** - Industry summary for monthly data

## Code Structure

### Before Optimization
- **~1200 lines** of code across 6 files
- **Duplicate functions** across files (date ranges, filtering, printing)
- **No orchestration** - had to run scripts manually

### After Optimization
- **~900 lines** of code (25% reduction)
- **40+ shared utilities** in utils.py
- **Single main.py** to run everything
- **Better maintainability** - changes in one place affect all modules

## Optimization Details

### What Was Removed (Redundant Code)
1. ❌ Duplicate `daterange()` function - now in utils.py
2. ❌ Duplicate `get_last_two_weeks()` function - now in utils.py
3. ❌ Duplicate `load_nifty50_symbols()` - now in utils.py
4. ❌ Duplicate column cleaning logic - now in `clean_dataframe()`
5. ❌ Duplicate `print_strong_stocks()` - parameterized in utils.py
6. ❌ Duplicate `print_strong_industries()` - shared in utils.py
7. ❌ Duplicate directory creation - centralized in `setup_directories()`
8. ❌ Duplicate filtering logic - `filter_nifty50_eq()` utility

### New Utilities Module

**utils.py** provides:
- Directory management
- NIFTY 50 data loading
- Data cleaning & normalization
- Date utilities
- Data filtering (NIFTY 50, EQ series)
- Data aggregation
- Comparison operations
- Industry data merging
- Output formatting
- CSV operations

## Module Responsibilities (After Refactoring)

| Module | Lines | Responsibility |
|--------|-------|-----------------|
| **download_bhavcopy.py** | 30 | Download NSE files |
| **filter_nifty50.py** | 20 | Filter NIFTY 50 symbols |
| **weekly_compare.py** | 55 | Weekly stock analysis |
| **weekly_industry_compare.py** | 40 | Weekly industry analysis |
| **monthly_compare.py** | 70 | Monthly stock analysis |
| **monthly_industry_compare.py** | 35 | Monthly industry analysis |
| **utils.py** | 280 | Shared utilities |
| **main.py** | 85 | Pipeline orchestration |

## How to Extend

### Add a new analysis module?
1. Create your module
2. Import utilities from `utils.py`
3. Add it to `main.py`
4. Done! No need to rewrite common logic

### Change thresholds?
1. Edit `print_strong_stocks(threshold=1.2)` call
2. Edit `print_strong_industries(threshold=1.1)` call
3. All modules automatically use the new values

### Modify date ranges?
1. Edit `get_last_two_weeks()` or `get_last_two_completed_months()` in utils.py
2. All modules automatically use the new logic

## Testing Individual Components

```bash
# Test data download
python3 download_bhavcopy.py

# Test filtering
python3 filter_nifty50.py

# Test weekly analysis
python3 weekly_compare.py
python3 weekly_industry_compare.py

# Test monthly analysis
python3 monthly_compare.py
python3 monthly_industry_compare.py
```

## Performance Notes

- **First run**: Slower (downloads ~10 NSE files)
- **Subsequent runs**: Cached files speed up processing
- **Monthly analysis**: Auto-downloads files if not present
- **Typical execution time**: 2-5 minutes depending on network

## Troubleshooting

### "Module not found" error
- Make sure all scripts are in the same directory
- Ensure `utils.py` is present

### "No dates loaded" message
- Verify NSE files are in `data/raw/` directory
- Check file naming format: `sec_bhavdata_full_DDMMYYYY.csv`

### Empty output files
- Verify `data/nifty50.csv` exists with correct Symbol column
- Check that dates are trading days (Mon-Fri)
- Verify raw CSV files are not corrupted

---

**Version**: 2.0 (Refactored)  
**Last Updated**: March 2026
