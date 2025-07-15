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
    zip_file = os.getenv("ZIP_DATA_FILE", "sample_zips.csv")
    
    if not os.path.exists(zip_file):
        print(f"⚠️  ZIP data file {zip_file} not found")
        # Try alternate file
        alternate_file = "sample_zips.csv" if zip_file != "sample_zips.csv" else "uszips.csv"
        if os.path.exists(alternate_file):
            print(f"🔄 Using alternate ZIP data file {alternate_file}")
            zip_file = alternate_file
        else:
            print("❌ No ZIP data file available")
            return {}
    
    try:
        # Load shapefile
        gdf = gpd.read_file(shapefile_path)
        gdf['ZCTA5CE20'] = gdf['ZCTA5CE20'].astype(str).str.zfill(5)
        gdf = gdf.set_index('ZCTA5CE20')
        
        with open(zip_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zip_code = str(row['zip']).zfill(5)
                
                # Check if the ZIP code exists in the shapefile
                if zip_code in gdf.index:
                    polygon = gdf.loc[zip_code]['geometry']
                    points = generate_grid_from_polygon(polygon, n_points)
                    zip_grid[zip_code] = points
                else:
                    print(f"⚠️  ZIP code {zip_code} not found in shapefile")
                    continue
                
    except Exception as e:
        print(f"❌ Error loading ZIP grid data: {e}")
        return {}
    
    return zip_grid