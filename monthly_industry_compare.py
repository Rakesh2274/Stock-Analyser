import os
import pandas as pd
from utils import setup_directories, print_strong_industries, save_csv

INPUT_FILE = "data/output/monthly_comparison.csv"
OUTPUT_DIR = "data/output"

setup_directories()


def main():
    df = pd.read_csv(INPUT_FILE)

    grouped = df.groupby("Industry").agg(
        SUM_TTL_TRD_QNTY_M1=("SUM_TTL_TRD_QNTY_M1", "sum"),
        SUM_TTL_TRD_QNTY_M2=("SUM_TTL_TRD_QNTY_M2", "sum"),
        SUM_DELIV_QTY_M1=("SUM_DELIV_QTY_M1", "sum"),
        SUM_DELIV_QTY_M2=("SUM_DELIV_QTY_M2", "sum"),
    ).reset_index()

    grouped["TTL_TRD_RATIO"] = (
        grouped["SUM_TTL_TRD_QNTY_M2"] /
        grouped["SUM_TTL_TRD_QNTY_M1"]
    )

    grouped["DELIV_RATIO"] = (
        grouped["SUM_DELIV_QTY_M2"] /
        grouped["SUM_DELIV_QTY_M1"]
    )

    output_path = os.path.join(OUTPUT_DIR, "monthly_industry_comparison.csv")
    save_csv(grouped, output_path)
    print_strong_industries(grouped)