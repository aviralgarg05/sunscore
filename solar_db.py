import csv
import os
from datetime import datetime, timedelta

OUTPUT_PATH = './data/solar_data.csv'

def save_solar_record(lat, lon, ghi_list, dni_list, dhi_list, year="2024", interval_minutes=30):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    base_time = datetime.strptime(f"{year}-01-01 00:00", "%Y-%m-%d %H:%M")

    with open(OUTPUT_PATH, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header only if file is empty
        if f.tell() == 0:
            writer.writerow(["Latitude", "Longitude", "Datetime", "GHI", "DNI", "DHI"])

        for i, (ghi, dni, dhi) in enumerate(zip(ghi_list, dni_list, dhi_list)):
            timestamp = base_time + timedelta(minutes=i * interval_minutes)
            writer.writerow([lat, lon, timestamp.strftime("%Y-%m-%d %H:%M"), ghi, dni, dhi])