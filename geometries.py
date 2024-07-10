"""import geopandas as gpd

# Load the shapefile
shapefile_path = 'DISTRICT_BOUNDARY.shp'
gdf = gpd.read_file(shapefile_path)

# Print the GeoDataFrame to inspect the data
print(gdf.head())
# print(gdf.columns)

# Print the first few rows of the GeoDataFrame, including all columns
print(gdf.head())
"""
"""
import geopandas as gpd

# Load the shapefile
shapefile_path = 'DISTRICT_BOUNDARY.shp'
gdf = gpd.read_file(shapefile_path)

# Print the number of geometries
print("Number of geometries:", len(gdf))
"""

print("Number of geometries:", len(gdf))
print("Number of district names:", len(district_names))
