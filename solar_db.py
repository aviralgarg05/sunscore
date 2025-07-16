import os
import csv
import uuid
from datetime import datetime
from pymongo import MongoClient

def save_solar_record(zip_code, lat, lon, records, year=None, in_docker=False):
    """
    Save solar irradiance records to MongoDB and/or CSV.
    """

    # Load MONGODB_URI and DB/COLLECTION names at runtime
    MONGO_URI = os.getenv("MONGODB_URI")
    MONGO_DB = os.getenv("MONGODB_DATABASE", "sunscore")
    MONGO_COLLECTION = os.getenv("MONGODB_COLLECTION", "solar_data")
    if not MONGO_URI:
        print(f"[⚠️] No MONGO_URI configured. Skipping MongoDB upload. (MONGO_URI={MONGO_URI})")
    else:
        try:
            print(f"[ℹ️] Connecting to MongoDB at {MONGO_URI} ...")
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
            client.admin.command('ping')
            db = client[MONGO_DB]
            collection = db[MONGO_COLLECTION]

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

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()