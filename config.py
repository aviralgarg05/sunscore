# config.py

from dotenv import load_dotenv
load_dotenv()

import os

API_KEY = os.getenv("NSRDB_API_KEY")
EMAIL = os.getenv("NSRDB_EMAIL")
YEAR = os.getenv("NSRDB_YEAR", "2024")
ZIP_DATA_FILE = os.getenv("ZIP_DATA_FILE", "zip_codes.csv")

if not API_KEY:
    raise ValueError("NSRDB_API_KEY environment variable is required")

if not EMAIL:
    raise ValueError("NSRDB_EMAIL environment variable is required")