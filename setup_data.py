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
        'sample_zips.csv': 'ZIP codes database with lat/lng coordinates (sample)',
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
    """Create a sample ZIP code data file for testing."""
    print("📝 Creating sample ZIP code data...")
    
    sample_file = 'sample_zips.csv'
    sample_data = [
        ["zip", "lat", "lng", "city", "state_id", "state_name", "county_fips", "county_name", "timezone"],
        ["90210", "34.0901", "-118.4065", "Beverly Hills", "CA", "California", "06037", "Los Angeles", "America/Los_Angeles"],
        ["10001", "40.7501", "-73.9964", "New York", "NY", "New York", "36061", "New York", "America/New_York"],
        ["60601", "41.8855", "-87.6214", "Chicago", "IL", "Illinois", "17031", "Cook", "America/Chicago"],
        ["98101", "47.6097", "-122.3331", "Seattle", "WA", "Washington", "53033", "King", "America/Los_Angeles"],
        ["33139", "25.7820", "-80.1341", "Miami Beach", "FL", "Florida", "12086", "Miami-Dade", "America/New_York"]
    ]
    
    try:
        with open(sample_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        print(f"✅ Created {sample_file} with {len(sample_data)-1} sample ZIP codes")
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

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
