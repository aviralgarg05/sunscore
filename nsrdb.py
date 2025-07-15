import requests
import time
from typing import Tuple, Optional

def get_solar_data(lat: float, lon: float, year: str, email: str, api_key: str) -> Tuple[bool, Optional[float], Optional[float], Optional[float]]:
    """
    Fetch solar irradiance data from NREL NSRDB API.
    
    Returns:
        Tuple of (success, ghi, dni, dhi)
    """
    url = "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv"
    
    params = {
        'wkt': f'POINT({lon} {lat})',
        'names': year,
        'attributes': 'ghi,dni,dhi',
        'email': email,
        'api_key': api_key,
        'utc': 'false',
        'leap_day': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Parse the CSV response
        lines = response.text.strip().split('\n')
        
        # Find the data section (skip metadata)
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith('Year,Month,Day'):
                data_start = i + 1
                break
        
        if data_start == 0:
            print(f"❌ No data header found in response")
            return False, None, None, None
        
        # Calculate averages from the data
        ghi_sum = dni_sum = dhi_sum = 0
        count = 0
        
        for line in lines[data_start:data_start + 100]:  # Sample first 100 rows
            if not line.strip():
                continue
                
            try:
                parts = line.split(',')
                if len(parts) >= 8:
                    ghi = float(parts[5])
                    dni = float(parts[6])
                    dhi = float(parts[7])
                    
                    ghi_sum += ghi
                    dni_sum += dni
                    dhi_sum += dhi
                    count += 1
                    
            except (ValueError, IndexError):
                continue
        
        if count == 0:
            print(f"❌ No valid data rows found")
            return False, None, None, None
        
        # Return averages
        avg_ghi = ghi_sum / count
        avg_dni = dni_sum / count
        avg_dhi = dhi_sum / count
        
        print(f"✅ Got solar data: GHI={avg_ghi:.2f}, DNI={avg_dni:.2f}, DHI={avg_dhi:.2f}")
        return True, avg_ghi, avg_dni, avg_dhi
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False, None, None, None
    except Exception as e:
        print(f"❌ Error processing solar data: {e}")
        return False, None, None, None