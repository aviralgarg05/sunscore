import os
import time
from dotenv import load_dotenv
from zip_grid import get_zip_latlon_grid
from nsrdb import get_solar_data
from solar_db import save_solar_record
from zip_loader import load_usa_zip_list

# Load environment variables
load_dotenv()

API_KEY = os.getenv("NSRDB_API_KEY")
EMAIL = os.getenv("NSRDB_EMAIL")
YEAR = os.getenv("NSRDB_YEAR", "2024")
ZIP_DATA_FILE = os.getenv("ZIP_DATA_FILE", "sample_zips.csv")
IN_DOCKER = os.environ.get('DOCKER_CONTAINER', 'false').lower() == 'true'

print(f"🔑 API Key present: {'Yes' if API_KEY else 'No'}")
print(f"📧 Email present: {'Yes' if EMAIL else 'No'}")
print(f"📅 Year: {YEAR}")
print(f"📁 ZIP file: {ZIP_DATA_FILE}")
print(f"🐳 Running in Docker: {'Yes' if IN_DOCKER else 'No (will save to local CSV)'}")

if not API_KEY or not EMAIL:
    print("❌ Missing required environment variables:")
    if not API_KEY:
        print("  - NSRDB_API_KEY is not set")
    if not EMAIL:
        print("  - NSRDB_EMAIL is not set")
    raise ValueError("NSRDB_API_KEY and NSRDB_EMAIL must be set in .env file")

UNSUPPORTED_STATES = {"PR", "VI", "GU", "AS", "MP"}

def main():
    print("[⚙️] Starting Sunscore Data Scraper...")

    if not os.path.exists(ZIP_DATA_FILE):
        print(f"❌ ZIP data file not found: {ZIP_DATA_FILE}")
        return

    zip_data = load_usa_zip_list(ZIP_DATA_FILE)
    if not zip_data:
        print("❌ No ZIP data loaded. Please check your ZIP codes file.")
        return

    print(f"📊 Loaded {len(zip_data)} ZIP codes")
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

        for i, (lat, lon) in enumerate(latlon_list):
            print(f"[🌞] Trying {zip_code} @{lat:.6f}, {lon:.6f} ({i+1}/{len(latlon_list)})...")

            try:
                success, records = get_solar_data(lat, lon, YEAR, EMAIL, API_KEY)

                if success and records:
                    save_solar_record(
                        zip_code=zip_code,
                        lat=lat,
                        lon=lon,
                        records=records,
                        year=YEAR,
                        in_docker=IN_DOCKER
                    )
                    print(f"✅ Saved {len(records)} records for ZIP {zip_code} point #{i+1}")
                else:
                    print(f"❌ No data for ZIP {zip_code} point #{i+1}")

                time.sleep(1)  # Rate limiting

            except Exception as e:
                print(f"⚠️ Error processing ZIP {zip_code} point #{i+1}: {e}")

if __name__ == "__main__":
    main()