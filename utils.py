import csv
from io import StringIO

def parse_solar_csv(raw_csv, zip_code, lat, lon, city, state):
    lines = raw_csv.strip().splitlines()
    reader = csv.reader(lines)

    # Skip metadata lines
    while not next(reader)[0].startswith("Year"):
        pass

    header = next(reader)
    data_rows = []

    for row in reader:
        year, month, day, hour, minute, ghi, dni, dhi = row
        data_rows.append([
            zip_code, city, state, lat, lon,
            int(year), int(month), int(day),
            int(hour), int(minute),
            float(ghi), float(dni), float(dhi)
        ])

    return data_rows

def save_to_csv(filename, data_rows):
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data_rows)

def log_failure(filename, zip_code, lat, lon, state, city):
    with open(filename, "a") as f:
        f.write(f"{zip_code},{lat},{lon},{state},{city}\n")