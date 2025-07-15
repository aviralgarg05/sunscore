import requests
import time
from typing import Tuple, List

def get_solar_data(lat: float, lon: float, year: str, email: str, api_key: str) -> Tuple[bool, List[dict]]:
    """
    Fetch detailed hourly solar data from NSRDB API for a given lat/lon.
    Returns success flag and list of records.
    Each record includes: {year, month, day, hour, minute, ghi, dni, dhi}
    """
    url = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv"

    params = {
        'wkt': f'POINT({lon} {lat})',
        'names': year,
        'attributes': 'ghi,dni,dhi',
        'email': email,
        'api_key': api_key,
        'utc': 'false',
        'leap_day': 'true'
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        lines = response.text.strip().split('\n')
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith('Year,Month,Day'):
                data_start = i
                break

        if data_start == 0:
            print("❌ No data header found in response")
            return False, []

        headers = lines[data_start].split(',')
        data_lines = lines[data_start + 1:]
        records = []

        for line in data_lines:
            if not line.strip():
                continue

            try:
                parts = line.split(',')
                record = {
                    'year': int(parts[0]),
                    'month': int(parts[1]),
                    'day': int(parts[2]),
                    'hour': int(parts[3]),
                    'minute': int(parts[4]),
                    'ghi': float(parts[5]),
                    'dni': float(parts[6]),
                    'dhi': float(parts[7]),
                }
                records.append(record)
            except Exception as e:
                continue

        if not records:
            print("❌ No valid data rows found")
            return False, []

        print(f"✅ Got {len(records)} solar data rows")
        return True, records

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False, []
    except Exception as e:
        print(f"❌ Error processing solar data: {e}")
        return False, []