import os
import pandas as pd
from utils import (
    setup_directories, convert_numeric_columns, load_nifty50_data,
    compare_two_periods, add_industry_data, print_strong_stocks, save_csv,
    get_last_two_weeks
)

INPUT_FILE = "data/processed/filtered_combined.csv"
OUTPUT_DIR = "data/output"

setup_directories()


def load_data():
    df = pd.read_csv(INPUT_FILE)
    df.columns = df.columns.str.strip()
    df["DATE1"] = df["DATE1"].str.strip()
    df["DATE1"] = pd.to_datetime(df["DATE1"], format="%d-%b-%Y")
    df = convert_numeric_columns(df, ["TTL_TRD_QNTY", "DELIV_QTY"])
    return df


def split_weeks(df):
    """Split data into last 2 calendar weeks based on actual download dates"""
    df = df.sort_values("DATE1")
    
    # Get the actual last 2 weeks that were downloaded
    week1_dates, week2_dates = get_last_two_weeks()
    
    # Extract only the dates from our dataframe (remove time component)
    df["DATE_ONLY"] = df["DATE1"].dt.date
    
    print("Last 2 Weeks Date Ranges:")
    print(f"Week1: {week1_dates[0].date()} to {week1_dates[-1].date()} ({len(week1_dates)} files)")
    print(f"Week2: {week2_dates[0].date()} to {week2_dates[-1].date()} ({len(week2_dates)} files)")
    
    # Print the raw files used for each week (these are the actual dates being analyzed)
    print("\nWeek1 Raw Files Being Processed:")
    for date in week1_dates:
        filename = f"sec_bhavdata_full_{date.strftime('%d%m%Y')}.csv"
        print(f"  • {filename}")

    print("\nWeek2 Raw Files Being Processed:")
    for date in week2_dates:
        filename = f"sec_bhavdata_full_{date.strftime('%d%m%Y')}.csv"
        print(f"  • {filename}")

    week1 = df[df["DATE_ONLY"].isin([d.date() for d in week1_dates])]
    week2 = df[df["DATE_ONLY"].isin([d.date() for d in week2_dates])]
    
    # Drop the helper column
    df = df.drop("DATE_ONLY", axis=1)

    return week1, week2


def aggregate_week(df):
    grouped = df.groupby("SYMBOL").agg(
        SUM_TTL_TRD_QNTY=("TTL_TRD_QNTY", "sum"),
        SUM_DELIV_QTY=("DELIV_QTY", "sum")
    ).reset_index()
    return grouped


def main():
    df = load_data()
    week1, week2 = split_weeks(df)

    week1_summary = aggregate_week(week1)
    week2_summary = aggregate_week(week2)

    save_csv(week1_summary, os.path.join("data/processed", "week1_summary.csv"))
    save_csv(week2_summary, os.path.join("data/processed", "week2_summary.csv"))

    # Compare weeks
    merged = compare_two_periods(week1_summary, week2_summary, ("WEEK1", "WEEK2"))
    
    # Add industry data
    nifty = load_nifty50_data()
    merged = add_industry_data(merged, nifty)

    # Save and print results
    output_path = os.path.join(OUTPUT_DIR, "weekly_comparison.csv")
    save_csv(merged, output_path)
    print_strong_stocks(merged)


if __name__ == "__main__":
    main()