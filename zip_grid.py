import csv
import os
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon
from typing import Dict, List, Tuple

def generate_grid_from_polygon(polygon: Polygon, n_points: int = 50) -> List[Tuple[float, float]]:
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < n_points:
        randx = np.random.uniform(minx, maxx)
        randy = np.random.uniform(miny, maxy)
        p = gpd.points_from_xy([randx], [randy])[0]
        if polygon.contains(p):
            points.append((randy, randx))
    return points

def get_zip_latlon_grid(shapefile_path: str = './shapefiles/tl_2023_us_zcta520.shp', n_points: int = 50) -> Dict[str, List[Tuple[float, float]]]:
    """
    Returns a dictionary mapping ZIP codes to lists of (lat, lon) coordinate pairs.
    This creates a simple grid of coordinates for each ZIP code.
    """
    zip_grid = {}
    
    # Try to load from the ZIP data file
    zip_file = os.getenv("ZIP_DATA_FILE", "uszips.csv")
    
    if not os.path.exists(zip_file):
        print(f"⚠️  ZIP data file {zip_file} not found")
        return {}
    
    try:
        with open(zip_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zip_code = str(row['zip']).zfill(5)
                lat = float(row['lat'])
                lng = float(row['lng'])
                
                # Create a simple grid around the ZIP code center
                # For now, we'll just use the center point
                zip_grid[zip_code] = [(lat, lng)]
                
    except Exception as e:
        print(f"❌ Error loading ZIP grid data: {e}")
        return {}
    
    return zip_grid

def create_sample_zip_grid() -> Dict[str, List[Tuple[float, float]]]:
    """Create sample ZIP grid data for testing."""
    return {
        "10001": [(40.7505, -73.9934)],  # NYC
        "90210": [(34.0901, -118.4065)], # Beverly Hills
        "60601": [(41.8781, -87.6298)],  # Chicago
        "33101": [(25.7617, -80.1918)],  # Miami
        "94102": [(37.7749, -122.4194)]  # San Francisco
    }