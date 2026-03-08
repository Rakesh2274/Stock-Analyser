# Stock Analyser - Refactored Pipeline

## Overview
This is an optimized stock analysis tool that analyzes NSE NIFTY 50 stocks for institutional accumulation patterns based on delivery ratios and trading volumes.

## Architecture

### New Structure
```
stock-analyser/
├── main.py                          # Main pipeline orchestrator
├── utils.py                         # Shared utilities (NEW)
├── download_bhavcopy.py             # Download NSE data (refactored)
├── filter_nifty50.py                # Filter NIFTY 50 stocks (refactored)
├── weekly_compare.py                # Weekly stock comparison (refactored)
├── weekly_industry_compare.py       # Weekly industry analysis (refactored)
├── monthly_compare.py               # Monthly stock comparison (refactored)
├── monthly_industry_compare.py      # Monthly industry analysis (refactored)
└── data/
    ├── nifty50.csv
    ├── raw/                         # Downloaded CSV files
    ├── processed/                   # Filtered & aggregated data
    └── output/                      # Final comparison results
```

## Key Improvements

### 1. **Eliminated Code Duplication**
   - **utils.py** contains 40+ shared functions used across all modules
   - Column cleaning, directory setup, date ranges, data filtering
   - Print functions for stocks and industries
   - Data loading and CSV operations

### 2. **Unified Data Processing**
   - All modules use `clean_dataframe()` for consistent data cleaning
   - Reusable aggregation and comparison logic
   - Standardized numeric column conversion
   - Centralized NIFTY 50 symbol loading

### 3. **Simplified Module Structure**
   - Each module focused on single responsibility
   - ~60% less code in individual files
   - No more duplicate date range functions
   - No more duplicate filtering logic

### 4. **Main Pipeline Orchestration**
   - **main.py** runs all steps sequentially
   - Clear progress tracking with formatted headers
   - Proper error handling and exit codes
   - Easy to modify pipeline order if needed

## Pipeline Flow

```
main.py
├── Step 1: Setup Directories
├── Step 2: Download 2 Weeks of Data (download_bhavcopy.py)
├── Step 3: Filter NIFTY 50 Stocks (filter_nifty50.py)
├── Step 4: Weekly Stock Analysis (weekly_compare.py)
├── Step 5: Weekly Industry Analysis (weekly_industry_compare.py)
├── Step 6: Monthly Stock Analysis (monthly_compare.py)
└── Step 7: Monthly Industry Analysis (monthly_industry_compare.py)
```

## Usage

### Run Complete Pipeline
```bash
python3 main.py
```

This will:
1. Download NSE data for 2 weeks
2. Filter NIFTY 50 stocks
3. Analyze weekly trends (stocks & industries)
4. Download and analyze monthly trends (stocks & industries)
5. Generate 4 comparison CSV files in `data/output/`

### Run Individual Modules
```bash
# Download only
python3 download_bhavcopy.py

# Filter only
python3 filter_nifty50.py

# Weekly analysis only
python3 weekly_compare.py
python3 weekly_industry_compare.py

# Monthly analysis only
python3 monthly_compare.py
python3 monthly_industry_compare.py
```

## Output Files

### Weekly Analysis
- **weekly_comparison.csv** - Stock-level metrics comparing Week 1 vs Week 2
- **weekly_industry_comparison.csv** - Industry-level aggregation

### Monthly Analysis
- **monthly_comparison.csv** - Stock-level metrics comparing Month 1 vs Month 2
- **monthly_industry_comparison.csv** - Industry-level aggregation

### Columns in Comparison Files
- `SYMBOL` - Stock ticker
- `Industry` - Sector/industry
- `SUM_TTL_TRD_QNTY_*` - Total trading quantity
- `SUM_DELIV_QTY_*` - Delivery quantity (institutional holdings)
- `TTL_TRD_RATIO` - Trading volume ratio (Period2/Period1)
- `DELIV_RATIO` - Delivery ratio (institutional buying indicator)

## Key Metrics

### Delivery Ratio
- Shows institutional accumulation (>1.0 = increasing holdings)
- Higher values indicate stronger buying by institutions

### Volume Ratio
- Shows trading activity change (>1.0 = increased volume)
- Useful to filter out stocks with very low volume

### Strong Stocks Threshold
- Volume Ratio > 1.2 (20% increase)
- Used to identify developing trends

### Strong Industries Threshold
- Volume Ratio > 1.1 (10% increase)
- Industry-level accumulation patterns

## Dependencies

```
pandas
requests
```

## Notes

- All scripts now import from `utils.py` for common operations
- Consistent error handling and logging throughout
- Uses reference_date parameter for testing (defaults to today)
- NSE files are cached - won't re-download if already present

## ENV AND RUN COMMAND 

# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Run
python3 main.py > output.log 2>&1