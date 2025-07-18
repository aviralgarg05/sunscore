import os
import csv
from datetime import datetime
import boto3
from botocore.config import Config

def save_solar_record(zip_code, lat, lon, records, year=None, in_docker=False):
    """
    Save solar irradiance records to CSV and upload to Tebi S3.
    """

    # Save to CSV outside Docker
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

    # Upload to Tebi S3
    try:
        access_key = os.getenv("TEBI_ACCESS_KEY_ID")
        secret_key = os.getenv("TEBI_SECRET_ACCESS_KEY")
        bucket = os.getenv("TEBI_BUCKET_NAME")
        # Use HTTP instead of HTTPS to avoid SSL validation error for buckets with dots
        endpoint = os.getenv("TEBI_ENDPOINT_URL", "http://s3.tebi.io").replace("https://", "http://")
        region = os.getenv("TEBI_REGION", "us-east-1")

        if not all([access_key, secret_key, bucket, endpoint]):
            print("[⚠️] Missing Tebi S3 configuration in environment variables.")
            return

        s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint,
            region_name=region,
            config=Config(s3={"addressing_style": "path"})
        )

        with open("solar_data.csv", "rb") as f:
            data = f.read()
            s3.put_object(
                Bucket=bucket,
                Key="solar_data.csv",
                Body=data,
                ContentLength=len(data)
            )
        print(f"[☁️] Uploaded solar_data.csv to Tebi S3 bucket '{bucket}' using path-style addressing and HTTP endpoint")

    except Exception as e:
        print(f"[❌] Tebi S3 upload error: Failed to upload solar_data.csv to {bucket}/solar_data.csv: {e}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()