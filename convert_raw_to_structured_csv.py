import csv
from datetime import datetime, timedelta
import os

def convert_raw_to_structured_csv(
    raw_file: str = "raw_solar_data.csv",
    output_file: str = "solar_data_structured.csv",
    start_time: str = "2024-01-01 00:00",
    interval_minutes: int = 30
):
    """Convert raw solar readings to structured CSV format with timestamps."""
    
    if not os.path.exists(raw_file):
        raise FileNotFoundError(f"[❌] File not found: {raw_file}")

    with open(raw_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        writer.writerow(["Latitude", "Longitude", "Datetime", "GHI", "DNI", "DHI"])

        base_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")

        for i, row in enumerate(reader):
            try:
                lat = float(row[0])
                lon = float(row[1])
                ghi = float(row[2])
                dni = float(row[3])
                dhi = float(row[4])
                timestamp = base_time + timedelta(minutes=i * interval_minutes)
                writer.writerow([lat, lon, timestamp.strftime("%Y-%m-%d %H:%M"), ghi, dni, dhi])
            except Exception as e:
                print(f"[⚠️] Skipping row {i+1}: {e}")

    print(f"✅ Successfully created: {output_file}")

# Optional: Auto-run when script is executed directly
if __name__ == "__main__":
    convert_raw_to_structured_csv(
        raw_file="raw_solar_data.csv",               # input file
        output_file="solar_data_structured.csv",     # output file
        start_time="2024-01-01 00:00",                # start timestamp
        interval_minutes=30                          # interval per row
    )