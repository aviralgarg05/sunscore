import csv
import os
from datetime import datetime, timedelta
from pymongo import MongoClient
import logging

OUTPUT_PATH = './data/solar_data.csv'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolarDB:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.database_name = os.getenv("DATABASE", "SunscoreData")
        self.collection_name = os.getenv("COLLECTION", "SolarData")
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logger.info(f"✅ Connected to MongoDB: {self.database_name}.{self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def save_record(self, lat: float, lon: float, ghi: float, dni: float, dhi: float, year: str):
        """Save solar data record to MongoDB."""
        if not self.collection:
            if not self.connect():
                return False
        
        record = {
            "latitude": lat,
            "longitude": lon,
            "ghi": ghi,
            "dni": dni,
            "dhi": dhi,
            "year": year,
            "timestamp": datetime.utcnow(),
            "location": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }
        
        try:
            result = self.collection.insert_one(record)
            logger.info(f"✅ Saved record with ID: {result.inserted_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save record: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()

# Global instance
_solar_db = SolarDB()

def save_solar_record(lat: float, lon: float, ghi: float, dni: float, dhi: float, year: str = "2024"):
    """Save solar data record to database."""
    return _solar_db.save_record(lat, lon, ghi, dni, dhi, year)

def close_db():
    """Close database connection."""
    _solar_db.close()

def _save_to_csv(records):
    """Helper function to save records to CSV"""
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    file_exists = os.path.exists(OUTPUT_PATH)
    
    with open(OUTPUT_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or f.tell() == 0:
            writer.writerow(["Latitude", "Longitude", "Datetime", "GHI", "DNI", "DHI"])
        for r in records:
            writer.writerow([r["latitude"], r["longitude"], r["datetime"], r["ghi"], r["dni"], r["dhi"]])
    logger.info(f"📄 CSV: Appended {len(records)} records to {OUTPUT_PATH}")