import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('127_enr1.csv')

# List of columns to exclude from mean calculation
exclude_columns = ['psuedocode']

# Group by 'item_desc' and calculate mean (average) excluding specified columns
mean_data = df.drop(exclude_columns, axis=1).groupby('item_desc').mean()

# Iterate through each group and print item_desc : mean
for item_desc, mean_values in mean_data.iterrows():
    print(f"{item_desc} : {mean_values.mean()}")
