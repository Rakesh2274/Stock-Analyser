import os
import requests
from datetime import datetime
from utils import setup_directories, get_last_two_weeks

BASE_URL = "https://nsearchives.nseindia.com/products/content/"
SAVE_DIR = "data/raw"

setup_directories()


def download_file(date):
    date_str = date.strftime("%d%m%Y")
    filename = f"sec_bhavdata_full_{date_str}.csv"
    url = BASE_URL + filename

    save_path = os.path.join(SAVE_DIR, filename)

    if os.path.exists(save_path):
        print(f"Already exists: {filename}")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/csv,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive",
    }

    try:
        print(f"Downloading: {filename}")

        session = requests.Session()
        session.headers.update(headers)

        response = session.get(url, timeout=30)

        if response.status_code == 200 and len(response.content) > 1000:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Saved: {filename}")
        else:
            print(f"Failed or Empty: {filename}")

    except Exception as e:
        print(f"Error downloading {filename}: {e}")


def download_last_two_weeks(reference_date=None):
    week1, week2 = get_last_two_weeks(reference_date)

    print("Downloading Week 1")
    for date in week1:
        download_file(date)

    print("Downloading Week 2")
    for date in week2:
        download_file(date)


if __name__ == "__main__":
    # Example fixed date
    reference_date = datetime(2026, 2, 23)

    download_last_two_weeks(reference_date)