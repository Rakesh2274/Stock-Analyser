import os
import requests
import pandas as pd
from datetime import datetime

from utils import (
    setup_directories, convert_numeric_columns, daterange,
    get_last_two_completed_months, load_and_filter_period,
    aggregate_by_column, compare_two_periods, add_industry_data,
    load_nifty50_data, print_strong_stocks, save_csv
)

BASE_URL = "https://nsearchives.nseindia.com/products/content/"
RAW_DIR = "data/raw"
OUTPUT_DIR = "data/output"

setup_directories()


# ---------- DOWNLOAD SECTION ----------

def download_file(date):
    date_str = date.strftime("%d%m%Y")
    filename = f"sec_bhavdata_full_{date_str}.csv"
    filepath = os.path.join(RAW_DIR, filename)

    if os.path.exists(filepath):
        return

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.nseindia.com/",
    }

    url = BASE_URL + filename

    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200 and len(response.content) > 1000:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Failed: {filename}")


def download_month(month_range):
    for date in daterange(month_range[0], month_range[1]):
        download_file(date)


# ---------- MAIN ----------

def main():
    today = datetime.today()
    month1, month2 = get_last_two_completed_months(today)

    print(f"\nMonth1 (Older): {month1[0].date()} to {month1[1].date()}")
    print(f"Month2 (Recent): {month2[0].date()} to {month2[1].date()}")

    print("\nDownloading data...")
    download_month(month1)
    download_month(month2)

    print("\nProcessing data...")
    
    # Load and filter for each month
    m1_list = list(daterange(month1[0], month1[1]))
    m2_list = list(daterange(month2[0], month2[1]))
    
    m1_df, _ = load_and_filter_period(m1_list, "Month1 (Older)")
    m2_df, _ = load_and_filter_period(m2_list, "Month2 (Recent)")

    if m1_df.empty or m2_df.empty:
        print("Insufficient data")
        return

    # Convert numeric columns before aggregation
    m1_df = convert_numeric_columns(m1_df, ["TTL_TRD_QNTY", "DELIV_QTY"])
    m2_df = convert_numeric_columns(m2_df, ["TTL_TRD_QNTY", "DELIV_QTY"])
    
    # Aggregate by symbol
    m1 = aggregate_by_column(m1_df, "SYMBOL", ["TTL_TRD_QNTY", "DELIV_QTY"])
    m2 = aggregate_by_column(m2_df, "SYMBOL", ["TTL_TRD_QNTY", "DELIV_QTY"])
    
    # Rename columns for comparison
    m1.columns = ["SYMBOL", "SUM_TTL_TRD_QNTY_M1", "SUM_DELIV_QTY_M1"]
    m2.columns = ["SYMBOL", "SUM_TTL_TRD_QNTY_M2", "SUM_DELIV_QTY_M2"]

    # Compare months
    merged = compare_two_periods(m1, m2, ("M1", "M2"))
    
    # Add industry data
    nifty = load_nifty50_data()
    merged = add_industry_data(merged, nifty)

    # Save and print results
    output_path = os.path.join(OUTPUT_DIR, "monthly_comparison.csv")
    save_csv(merged, output_path)
    print_strong_stocks(merged)