import os
import csv
import uuid
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def save_solar_record(zip_code, lat, lon, records, year=None, in_docker=False):
    """
    Save solar irradiance records to MongoDB and/or CSV.
    """

    # Optional MongoDB upload
    if MONGO_URI:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
            db = client.sunscore
            collection = db.solar_data

            docs = []
            for rec in records:
                timestamp = datetime(rec["year"], rec["month"], rec["day"], rec["hour"], rec["minute"])
                doc = {
                    "_id": str(uuid.uuid4()),
                    "zip_code": zip_code,
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": timestamp,
                    "ghi": rec["ghi"],
                    "dni": rec["dni"],
                    "dhi": rec["dhi"],
                    "source": "NSRDB"
                }
                docs.append(doc)

            if docs:
                collection.insert_many(docs)
                print(f"[🗃️] Inserted {len(docs)} records to MongoDB for ZIP {zip_code}")

        except Exception as e:
            print(f"[❌] MongoDB error: {e}")
    else:
        print("[⚠️] No MONGO_URI configured. Skipping MongoDB upload.")

    # Save to CSV outside Docker
    if not in_docker:
        csv_path = "solar_data.csv"
        file_exists = os.path.exists(csv_path)
        fieldnames = [
            "zip_code", "latitude", "longitude",
            "year", "month", "day", "hour", "minute",
            "ghi", "dni", "dhi"
        ]

        try:
            with open(csv_path, mode="a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()

                for rec in records:
                    writer.writerow({
                        "zip_code": zip_code,
                        "latitude": lat,
                        "longitude": lon,
                        "year": rec["year"],
                        "month": rec["month"],
                        "day": rec["day"],
                        "hour": rec["hour"],
                        "minute": rec["minute"],
                        "ghi": rec["ghi"],
                        "dni": rec["dni"],
                        "dhi": rec["dhi"]
                    })

            print(f"[📄] Wrote {len(records)} rows to CSV for ZIP {zip_code}")

        except Exception as e:
            print(f"[❌] CSV write error: {e}")