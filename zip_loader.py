import csv
from typing import List, Dict

def load_usa_zip_list(filepath: str) -> List[Dict]:
    """
    Load ZIP code data from a CSV with at least the following columns:
    - zip
    - lat
    - lng  
    - state_id
    - city
    """
    zip_list = []
    
    # Check if file exists
    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    zip_list.append({
                        "zip": row["zip"].zfill(5),
                        "lat": float(row["lat"]),
                        "lng": float(row["lng"]),
                        "state_id": row["state_id"],
                        "city": row["city"]
                    })
                except (KeyError, ValueError) as e:
                    print(f"[⚠️] Skipping row due to error: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"❌ ZIP data file not found: {filepath}")
        print("💡 Run 'python setup_data.py' to create sample data")
        return []
    
    return zip_list