import csv
import os
import time
import requests
from utils import parse_solar_csv, save_to_csv, log_failure
from zip_loader import load_usa_zip_list
from config import API_KEY, EMAIL, YEAR

DATA_YEAR = YEAR
OUTPUT_CSV = "sunscore_data.csv"
FAIL_LOG = "sunscore_failures.log"

zip_data = load_usa_zip_list("uszips.csv")

# Setup output file once
if not os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ZIP", "City", "State", "Latitude", "Longitude",
            "Year", "Month", "Day", "Hour", "Minute", "GHI", "DNI", "DHI"
        ])

for i, entry in enumerate(zip_data[:5000]):
    zip_code = str(entry["zip"]).zfill(5)
    lat = round(entry["lat"], 5)
    lon = round(entry["lng"], 5)
    state = entry["state_id"]
    city = entry["city"]

    print(f"[🌞] Request {i+1}/5000 for ZIP {zip_code} ({lat}, {lon})...")

    url = (
        f"https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv?"
        f"wkt=POINT({lon}%20{lat})"
        f"&attributes=ghi,dni,dhi"
        f"&names={DATA_YEAR}"
        f"&utc=false&leap_day=true"
        f"&email={EMAIL}"
        f"&api_key={API_KEY}"
    )

    success = False
    for retry in range(3):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = parse_solar_csv(response.text, zip_code, lat, lon, city, state)
            save_to_csv(OUTPUT_CSV, data)
            print(f"✅ [ZIP {zip_code}] Saved {len(data)} rows")
            success = True
            break
        except Exception as e:
            print(f"🔁 Retry {retry+1} for ZIP {zip_code}...")
            time.sleep(2)

    if not success:
        print(f"❌ [ZIP {zip_code}] Failed.")
        log_failure(FAIL_LOG, zip_code, lat, lon, state, city)

    time.sleep(1)  # ✅ Rate limit: 1 req/sec