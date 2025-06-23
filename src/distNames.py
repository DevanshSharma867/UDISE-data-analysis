import geopandas as gpd
import csv 

# Assuming you have already read your GeoJSON file into gdf
geojson_file = "INDIA_DISTRICTS.geojson"
gdf = gpd.read_file(geojson_file)

# Print unique values in the 'dtname' column

with open("karnataka_districts.csv", "r", encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)  # Skip the header row
    # Process each row in the CSV
    for row in content:
        for info in row:
            print(info)
# for item in gdf['dtname'].unique():
    # print(item)
