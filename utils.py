import os
import pandas as pd
from datetime import datetime, timedelta

# ============ DIRECTORY SETUP ============

def setup_directories():
    """Create all necessary directories"""
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)


# ============ NIFTY 50 HELPERS ============

def load_nifty50_symbols():
    """Load NIFTY 50 symbols from CSV"""
    df = pd.read_csv("data/nifty50.csv")
    return set(df["Symbol"].str.strip())


def load_nifty50_data():
    """Load complete NIFTY 50 data with symbols and industries"""
    df = pd.read_csv("data/nifty50.csv")
    df.columns = df.columns.str.strip()
    return df


# ============ DATA CLEANING ============

def clean_dataframe(df):
    """
    Clean dataframe: strip whitespace from column names and common columns
    """
    df.columns = df.columns.str.strip()
    
    if "SYMBOL" in df.columns:
        df["SYMBOL"] = df["SYMBOL"].str.strip()
    if "SERIES" in df.columns:
        df["SERIES"] = df["SERIES"].str.strip()
    if "DATE1" in df.columns:
        df["DATE1"] = df["DATE1"].str.strip()
    
    return df


def convert_numeric_columns(df, columns):
    """Convert specified columns to numeric"""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col])
    return df


# ============ DATE UTILITIES ============

# NSE/Stock Market Holidays in 2026
NSE_HOLIDAYS_2026 = [
    datetime(2026, 1, 26),   # Republic Day
    datetime(2026, 3, 3),    # Holi
    datetime(2026, 3, 25),   # Ramzan Id
    datetime(2026, 4, 2),    # Good Friday
    datetime(2026, 4, 10),   # Eid ul-Adha
    datetime(2026, 4, 14),   # Ambedkar Jayanti
    datetime(2026, 8, 15),   # Independence Day
    datetime(2026, 8, 19),   # Janmashtami
    datetime(2026, 9, 2),    # Ganesh Chaturthi
    datetime(2026, 10, 2),   # Gandhi Jayanti
    datetime(2026, 10, 24),  # Diwali
    datetime(2026, 10, 25),  # Diwali (Day 2)
    datetime(2026, 10, 29),  # Guru Nanak Jayanti
    datetime(2026, 12, 25),  # Christmas
]

def daterange(start_date, end_date):
    """Generate weekday dates between start and end"""
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday-Friday only
            yield current
        current += timedelta(days=1)


def get_last_two_weeks(reference_date=None):
    """
    Get last 2 calendar weeks of trading days (Mon-Fri only).
    Automatically skips weekends and NSE holidays.
    Returns up to 10 files (up to 5 per week).
    
    Example: If today is March 7, 2026 (Saturday)
    Week1 (Previous): Feb 23-27 (Mon-Fri)
    Week2 (Current): Mar 2-6 (Mon-Fri, excluding Mar 3 holiday)
    Result: 9 files total
    """
    if reference_date is None:
        reference_date = datetime.today()
    
    # Convert to date-only to avoid time component mismatches
    reference_date = datetime.combine(reference_date.date(), datetime.min.time())

    # Find Monday of current week
    days_since_monday = reference_date.weekday()
    week2_monday = reference_date - timedelta(days=days_since_monday)
    
    # Previous week Monday (7 days before)
    week1_monday = week2_monday - timedelta(days=7)
    
    week1 = []
    week2 = []
    
    # Week 1: Mon-Fri (skip holidays)
    for i in range(5):
        date = week1_monday + timedelta(days=i)
        if date.weekday() < 5 and date not in NSE_HOLIDAYS_2026:  # Weekday AND not holiday
            week1.append(date)
    
    # Week 2: Mon-Fri (skip holidays)
    for i in range(5):
        date = week2_monday + timedelta(days=i)
        if date.weekday() < 5 and date not in NSE_HOLIDAYS_2026:  # Weekday AND not holiday
            week2.append(date)
    
    return week1, week2


def get_last_two_completed_months(reference_date=None):
    """Get date ranges for last 2 completed months"""
    if reference_date is None:
        reference_date = datetime.today()
    
    # Convert to date-only to avoid time component issues
    reference_date = datetime.combine(reference_date.date(), datetime.min.time())

    first_of_current_month = reference_date.replace(day=1)

    # Month2 = last completed month (recent)
    month2_end = first_of_current_month - timedelta(days=1)
    month2_start = month2_end.replace(day=1)

    # Month1 = previous month (older)
    month1_end = month2_start - timedelta(days=1)
    month1_start = month1_end.replace(day=1)

    return (month1_start, month1_end), (month2_start, month2_end)


# ============ DATA LOADING & FILTERING ============

def load_raw_file(filepath):
    """Load a raw NSE CSV file"""
    df = pd.read_csv(filepath)
    return clean_dataframe(df)


def filter_nifty50_eq(df, nifty50_symbols):
    """Filter dataframe for NIFTY 50 symbols and EQ series"""
    return df[
        (df["SERIES"] == "EQ") &
        (df["SYMBOL"].isin(nifty50_symbols))
    ]


def load_and_filter_period(date_list, label="Period"):
    """
    Load and filter files for a specific date range
    Returns aggregated dataframe and list of dates loaded
    """
    nifty50_symbols = load_nifty50_symbols()
    dfs = []
    dates_loaded = []

    for date in date_list:
        filename = f"sec_bhavdata_full_{date.strftime('%d%m%Y')}.csv"
        filepath = os.path.join("data/raw", filename)

        if not os.path.exists(filepath):
            continue

        dates_loaded.append(date)
        df = load_raw_file(filepath)
        filtered = filter_nifty50_eq(df, nifty50_symbols)
        dfs.append(filtered)

    # Debug info
    print(f"\n{label} Debug Info:")
    if dates_loaded:
        print(f"Start Date: {min(dates_loaded).date()}")
        print(f"End Date:   {max(dates_loaded).date()}")
        print(f"Total Trading Days: {len(dates_loaded)}")
    else:
        print("No dates loaded")

    if not dfs:
        return pd.DataFrame(), dates_loaded

    combined = pd.concat(dfs, ignore_index=True)
    return combined, dates_loaded


def aggregate_by_column(df, group_col, value_cols):
    """
    Aggregate dataframe by a column
    """
    agg_dict = {col: "sum" for col in value_cols}
    grouped = df.groupby(group_col).agg(agg_dict).reset_index()
    return grouped


# ============ COMPARISON UTILITIES ============

def compare_two_periods(df1, df2, period_label=("PERIOD1", "PERIOD2")):
    """
    Compare two aggregated dataframes
    Returns merged dataframe with ratios
    """
    merged = df1.merge(
        df2,
        on="SYMBOL",
        suffixes=(f"_{period_label[0]}", f"_{period_label[1]}")
    )

    # Calculate ratios
    col1 = f"SUM_TTL_TRD_QNTY_{period_label[0]}"
    col2 = f"SUM_TTL_TRD_QNTY_{period_label[1]}"
    merged["TTL_TRD_RATIO"] = merged[col2] / merged[col1]

    col1 = f"SUM_DELIV_QTY_{period_label[0]}"
    col2 = f"SUM_DELIV_QTY_{period_label[1]}"
    merged["DELIV_RATIO"] = merged[col2] / merged[col1]

    return merged


def add_industry_data(df, nifty50_df):
    """Merge industry information to dataframe"""
    return df.merge(
        nifty50_df[["Symbol", "Industry"]],
        left_on="SYMBOL",
        right_on="Symbol",
        how="left"
    ).drop(columns=["Symbol"], errors="ignore")


# ============ PRINTING & OUTPUT ============

def print_strong_stocks(df, threshold=1.2):
    """Print strong accumulation stocks"""
    strong = df[df["TTL_TRD_RATIO"] > threshold].copy()
    strong = strong.sort_values(by="TTL_TRD_RATIO", ascending=False)

    print("\n=== Strong Accumulation Stocks (Symbol Level) ===\n")

    if strong.empty:
        print("No stocks found")
        return

    for _, row in strong.iterrows():
        print(
            f"{row['SYMBOL']:15} "
            f"Delivery Ratio: {row['DELIV_RATIO']:.2f}  "
            f"Volume Ratio: {row['TTL_TRD_RATIO']:.2f}"
        )


def print_strong_industries(df, threshold=1.1):
    """Print strong industries"""
    strong = df[df["TTL_TRD_RATIO"] > threshold].copy()
    strong = strong.sort_values(by="TTL_TRD_RATIO", ascending=False)

    print("\n=== Strong Industries ===\n")

    if strong.empty:
        print("No industries found")
        return

    for _, row in strong.iterrows():
        print(
            f"{row['Industry']:30} "
            f"Delivery Ratio: {row['DELIV_RATIO']:.2f}  "
            f"Volume Ratio: {row['TTL_TRD_RATIO']:.2f}"
        )


def save_csv(df, filepath):
    """Save dataframe to CSV"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath}")
