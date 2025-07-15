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
    print("[🌐] Loading ZCTA shapefile from local disk...")
    gdf = gpd.read_file(shapefile_path).to_crs(epsg=4326)

    zip_grid = {}
    for _, row in gdf.iterrows():
        zip_code = row['ZCTA5CE20']
        geometry = row['geometry']
        if geometry and geometry.is_valid:
            zip_grid[zip_code] = generate_grid_from_polygon(geometry, n_points=n_points)
    return zip_grid