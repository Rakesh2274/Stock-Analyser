import os
import pandas as pd
from utils import setup_directories, print_strong_industries, save_csv

INPUT_FILE = "data/output/weekly_comparison.csv"
OUTPUT_DIR = "data/output"

setup_directories()


def load_data():
    """Load weekly comparison data"""
    df = pd.read_csv(INPUT_FILE)
    df.columns = df.columns.str.strip()
    return df


def aggregate_by_industry(df):
    """Aggregate weekly data at Industry level"""
    grouped = df.groupby("Industry").agg(
        SUM_TTL_TRD_QNTY_WEEK1=("SUM_TTL_TRD_QNTY_WEEK1", "sum"),
        SUM_TTL_TRD_QNTY_WEEK2=("SUM_TTL_TRD_QNTY_WEEK2", "sum"),
        SUM_DELIV_QTY_WEEK1=("SUM_DELIV_QTY_WEEK1", "sum"),
        SUM_DELIV_QTY_WEEK2=("SUM_DELIV_QTY_WEEK2", "sum")
    ).reset_index()
    return grouped


def compare_industry(grouped):
    """Calculate ratios and save"""
    grouped["TTL_TRD_RATIO"] = (
        grouped["SUM_TTL_TRD_QNTY_WEEK2"] /
        grouped["SUM_TTL_TRD_QNTY_WEEK1"]
    )

    grouped["DELIV_RATIO"] = (
        grouped["SUM_DELIV_QTY_WEEK2"] /
        grouped["SUM_DELIV_QTY_WEEK1"]
    )

    output_path = os.path.join(OUTPUT_DIR, "weekly_industry_comparison.csv")
    save_csv(grouped, output_path)
    print_strong_industries(grouped)


def main():
    print("Loading weekly comparison file...")
    df = load_data()

    print("Aggregating industry data...")
    grouped = aggregate_by_industry(df)

    print("Calculating industry ratios...")
    compare_industry(grouped)


if __name__ == "__main__":
    main()