import csv

def load_usa_zip_list(filepath):
    """
    Load ZIP code data from a CSV with at least the following columns:
    - zip
    - lat
    - lng
    - state_id
    - city
    """
    zip_list = []
    with open(filepath, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean + cast
            try:
                zip_list.append({
                    "zip": row["zip"].zfill(5),
                    "lat": float(row["lat"]),
                    "lng": float(row["lng"]),
                    "state_id": row["state_id"],
                    "city": row["city"]
                })
            except Exception as e:
                print(f"[⚠️] Skipping row due to error: {e}")
    return zip_list