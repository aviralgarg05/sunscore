import requests
import time

def get_solar_data(lat: float, lon: float, year: str, email: str, api_key: str):
    url = (
        f"https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv"
        f"?wkt=POINT({lon}%20{lat})&names={year}&attributes=ghi,dni,dhi"
        f"&leap_day=true&utc=false&api_key={api_key}&full_name=SunscoreApp&email={email}"
    )

    for attempt in range(3):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                lines = resp.text.splitlines()
                data_lines = [line for line in lines if line and not line.startswith(('Source', 'Year'))]
                ghi, dni, dhi = [], [], []
                for line in data_lines:
                    parts = line.split(',')
                    if len(parts) >= 8:
                        try:
                            ghi.append(float(parts[5]))
                            dni.append(float(parts[6]))
                            dhi.append(float(parts[7]))
                        except ValueError:
                            continue  # skip bad data
                return True, ghi, dni, dhi
            elif resp.status_code == 403:
                print(f"❌ 403 Forbidden for {lat:.5f},{lon:.5f} — likely unsupported region")
                return False, [], [], []
            else:
                print(f"🔁 retry {attempt+1} for {lat:.5f},{lon:.5f} => {resp.status_code}")
                time.sleep(1)
        except Exception as e:
            print(f"🔁 retry {attempt+1} for {lat:.5f},{lon:.5f} => {e}")
            time.sleep(1)
    return False, [], [], []