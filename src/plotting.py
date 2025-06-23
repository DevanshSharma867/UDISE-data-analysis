import pandas as pd
import geopandas as gpd

# Step 1: Read the CSV file to get the list of district names
csv_file = 'selected_districts.csv'
csv_data = pd.read_csv(csv_file)

# Assuming the header of the CSV is 'Unique Outputs'
district_names = csv_data['Unique Outputs'].str.lower().tolist()  # Convert to lowercase

# Step 2: Read the GeoJSON file to get the GeoDataFrame
geojson_file = 'INDIA_DISTRICTS.geojson'
gdf = gpd.read_file(geojson_file)

# Convert the 'dtname' column to lowercase for case-insensitive comparison
gdf['dtname'] = gdf['dtname'].str.lower()

# Step 3: Filter the GeoDataFrame based on the district names from the CSV file
filtered_gdf = gdf[gdf['dtname'].isin(district_names)]

# Step 4: Save the filtered GeoDataFrame as a new GeoJSON file
filtered_geojson_file = 'selected_districts.geojson'
filtered_gdf.to_file(filtered_geojson_file, driver='GeoJSON')

print(f"Filtered GeoJSON file saved as {filtered_geojson_file}")

# Step 5: Create a GeoDataFrame for the non-selected districts
non_selected_gdf = gdf[~gdf['dtname'].isin(district_names)]

# Step 6: Save the non-selected GeoDataFrame as a new GeoJSON file
non_selected_geojson_file = 'not_selected_districts.geojson'
non_selected_gdf.to_file(non_selected_geojson_file, driver='GeoJSON')

print(f"Non-selected GeoJSON file saved as {non_selected_geojson_file}")
