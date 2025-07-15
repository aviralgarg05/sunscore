import os
import time
from dotenv import load_dotenv
from zip_grid import get_zip_latlon_grid
from nsrdb import get_solar_data
from solar_db import save_solar_record
from zip_loader import load_usa_zip_list

load_dotenv()

API_KEY = os.getenv("NSRDB_API_KEY")
EMAIL = os.getenv("NSRDB_EMAIL")
YEAR = os.getenv("NSRDB_YEAR", "2024")
ZIP_DATA_FILE = os.getenv("ZIP_DATA_FILE", "zip_codes.csv")

if not API_KEY or not EMAIL:
    raise ValueError("NSRDB_API_KEY and NSRDB_EMAIL must be set in .env file")

UNSUPPORTED_STATES = {"PR", "VI", "GU", "AS", "MP"}  # Territories NSRDB doesn't support

def main():
    print("[⚙️] Starting Sunscore Data Scraper...")

    zip_data = load_usa_zip_list(ZIP_DATA_FILE)
    zip_grid = get_zip_latlon_grid()

    for zip_row in zip_data:
        zip_code = str(zip_row['zip']).zfill(5)
        state = zip_row['state_id']

        if state in UNSUPPORTED_STATES:
            print(f"⏭️ Skipping unsupported region ZIP {zip_code} ({state})")
            continue

        if zip_code not in zip_grid:
            print(f"[⚠️] Skipping {zip_code} — no polygon/grid data available")
            continue

        latlon_list = zip_grid[zip_code]
        success = False

        for i, (lat, lon) in enumerate(latlon_list):
            print(f"[🌞] Trying {zip_code} @{lat:.6f}, {lon:.6f} ({i+1}/{len(latlon_list)})...")

            try:
                success, ghi, dni, dhi = get_solar_data(lat, lon, YEAR, EMAIL, API_KEY)

                if success:
                    save_solar_record(lat, lon, ghi, dni, dhi, year=YEAR)
                    print(f"✅ Saved data for ZIP {zip_code} point #{i+1}")
                    break
                else:
                    print(f"❌ Failed to get data for ZIP {zip_code} point #{i+1} @({lat:.6f},{lon:.6f})")
                    
                # Rate limiting to avoid API throttling
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ Error processing ZIP {zip_code} point #{i+1}: {e}")
                continue

        if not success:
            print(f"[❌] All points failed for ZIP {zip_code}. No data saved.")

if __name__ == "__main__":
    main()