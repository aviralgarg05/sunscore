import os

API_KEY = os.getenv("NSRDB_API_KEY")
EMAIL = os.getenv("USER_EMAIL")
BASE_URL = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv"
YEAR = os.getenv("YEAR", "2017")
ATTRIBUTES = os.getenv("ATTRIBUTES", "ghi,dni,dhi")

# Validation
if not API_KEY:
    raise ValueError("NSRDB_API_KEY environment variable is required")
if not EMAIL:
    raise ValueError("USER_EMAIL environment variable is required")