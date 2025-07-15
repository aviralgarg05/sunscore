import csv

LOG_FILE = "logs.csv"

def extract_valid_data_rows(lines):
    """
    Extract only the actual solar data rows (skip metadata).
    Returns rows as lists: [Year, Month, Day, Hour, Minute, GHI, DNI, DHI]
    """
    data_started = False
    headers = []
    rows = []

    for line in lines:
        if not data_started:
            if line.startswith("Year"):
                headers = line.strip().split(",")
                data_started = True
            continue

        values = line.strip().split(",")
        if len(values) >= 8:
            row = [values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7]]
            rows.append(row)

    return rows