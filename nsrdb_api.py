import requests
from config import API_KEY, EMAIL, BASE_URL, ATTRIBUTES

def stream_nsrdb_csv(lat, lon, year="2024"):
    params = {
        "wkt": f"POINT({lon} {lat})",
        "attributes": ATTRIBUTES,
        "names": year,
        "utc": "false",
        "leap_day": "true",
        "email": EMAIL,
        "api_key": API_KEY,
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    url = f"{BASE_URL}?{query_string}"

    with requests.get(url, stream=True, timeout=10) as r:
        r.raise_for_status()
        for line in r.iter_lines(decode_unicode=True):
            if line:
                yield line