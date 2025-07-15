import csv
from typing import List, Dict

def load_usa_zip_list(filename: str) -> List[Dict]:
    """Load USA ZIP codes from CSV file."""
    zip_data = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zip_data.append({
                    'zip': row['zip'],
                    'lat': float(row['lat']),
                    'lng': float(row['lng']),
                    'state_id': row['state_id'],
                    'city': row['city']
                })
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Please ensure the ZIP codes file exists.")
        return []
    
    return zip_data