"""
Data setup utility for SunScore project.
Helps users download and verify required data files.
"""

import os
import sys
import requests
import csv
from pathlib import Path

def check_required_files():
    """Check if required data files exist."""
    required_files = {
        'uszips.csv': 'ZIP codes database with lat/lng coordinates',
        'tl_2023_us_zcta520.zip': 'US Census ZCTA shapefile (optional for grid generation)'
    }
    
    missing_files = []
    
    for file_name, description in required_files.items():
        if not os.path.exists(file_name):
            missing_files.append((file_name, description))
            print(f"❌ Missing: {file_name} - {description}")
        else:
            print(f"✅ Found: {file_name}")
    
    return len(missing_files) == 0

def create_sample_zip_data():
    """Create a small sample ZIP codes file for testing."""
    sample_data = [
        {"zip": "10001", "lat": 40.7505, "lng": -73.9934, "city": "New York", "state_id": "NY"},
        {"zip": "90210", "lat": 34.0901, "lng": -118.4065, "city": "Beverly Hills", "state_id": "CA"},
        {"zip": "60601", "lat": 41.8781, "lng": -87.6298, "city": "Chicago", "state_id": "IL"},
        {"zip": "33101", "lat": 25.7617, "lng": -80.1918, "city": "Miami", "state_id": "FL"},
        {"zip": "94102", "lat": 37.7749, "lng": -122.4194, "city": "San Francisco", "state_id": "CA"},
        {"zip": "02101", "lat": 42.3601, "lng": -71.0589, "city": "Boston", "state_id": "MA"},
        {"zip": "98101", "lat": 47.6062, "lng": -122.3321, "city": "Seattle", "state_id": "WA"},
        {"zip": "78701", "lat": 30.2672, "lng": -97.7431, "city": "Austin", "state_id": "TX"},
        {"zip": "30301", "lat": 33.7490, "lng": -84.3880, "city": "Atlanta", "state_id": "GA"},
        {"zip": "80202", "lat": 39.7392, "lng": -104.9903, "city": "Denver", "state_id": "CO"}
    ]
    
    # Create the expected filename from environment or default
    filename = os.getenv("ZIP_DATA_FILE", "uszips.csv")
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["zip", "lat", "lng", "city", "state_id"])
        writer.writeheader()
        writer.writerows(sample_data)
    
    print(f"✅ Created sample ZIP data: {filename}")
    print("📝 For production, download complete ZIP codes database from:")
    print("   https://simplemaps.com/data/us-zips")
    return True

def main():
    print("🔧 SunScore Data Setup Utility")
    print("=" * 40)
    
    # Load environment variables if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    if check_required_files():
        print("\n✅ All required files found!")
        return True
    else:
        print("\n⚠️  Some files are missing.")
        
        # Auto-create sample data when running in container or non-interactive mode
        if os.getenv('RUN_ENV') == 'docker' or not sys.stdin.isatty():
            print("🤖 Auto-creating sample data for testing...")
            return create_sample_zip_data()
        
        print("\nOptions:")
        print("1. Create sample data for testing")
        print("2. Exit and download files manually (see README.md)")
        
        try:
            choice = input("\nCreate sample data? (y/N): ").lower()
            if choice in ['y', 'yes']:
                return create_sample_zip_data()
        except (EOFError, KeyboardInterrupt):
            print("\n🤖 Creating sample data for automated setup...")
            return create_sample_zip_data()
        
        print("ℹ️  Exiting. Please download required files manually.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
