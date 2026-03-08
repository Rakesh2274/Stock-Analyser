import os
import pandas as pd
from utils import setup_directories, load_nifty50_symbols, clean_dataframe, filter_nifty50_eq, save_csv

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

setup_directories()


def filter_all_files():
    nifty50_symbols = load_nifty50_symbols()

    all_filtered = []

    for file in sorted(os.listdir(RAW_DIR)):
        if not file.endswith(".csv"):
            continue

        file_path = os.path.join(RAW_DIR, file)
        print(f"Processing: {file}")

        df = pd.read_csv(file_path)
        df = clean_dataframe(df)

        filtered = filter_nifty50_eq(df, nifty50_symbols)
        all_filtered.append(filtered)

    combined_df = pd.concat(all_filtered, ignore_index=True)

    output_path = os.path.join(PROCESSED_DIR, "filtered_combined.csv")
    save_csv(combined_df, output_path)
    print(f"Total rows: {len(combined_df)}")



if __name__ == "__main__":
    filter_all_files()
    