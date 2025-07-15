"""
Data setup utility for SunScore project.
Helps users download and verify required data files.
"""

import os
import requests
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
    sample_data = """zip,lat,lng,city,state_id,state_name,county_fips,county_name
10001,40.7505,-73.9934,New York,NY,New York,36061,New York
90210,34.0901,-118.4065,Beverly Hills,CA,California,06037,Los Angeles
60601,41.8827,-87.6233,Chicago,IL,Illinois,17031,Cook
75201,32.7767,-96.7970,Dallas,TX,Texas,48113,Dallas
33101,25.7617,-80.1918,Miami,FL,Florida,12086,Miami-Dade"""

    with open('sample_uszips.csv', 'w') as f:
        f.write(sample_data)
    
    print("✅ Created sample_uszips.csv for testing")
    print("📝 For production, replace with complete ZIP codes database")

def main():
    print("🔧 SunScore Data Setup Utility")
    print("=" * 40)
    
    if check_required_files():
        print("\n✅ All required files found!")
    else:
        print("\n⚠️  Some files are missing.")
        print("\nOptions:")
        print("1. Create sample data for testing")
        print("2. Download files manually (see data_structure_example.md)")
        
        choice = input("\nCreate sample data? (y/N): ").lower()
        if choice == 'y':
            create_sample_zip_data()

if __name__ == "__main__":
    main()
