import csv
from collections import defaultdict
import math
import statistics
import time
st = time.process_time()
# Dictionary to hold the pseudocode and corresponding item descriptions with their accumulated values (for 129_enr1.csv)
temp_item_desc = defaultdict(lambda: defaultdict(int))

# Open and process 129_enr1.csv
with open("129_enr1.csv", "r", encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)  # Skip the header row
    
    # Process each row in the CSV for pseudocodes from 129_enr1.csv
    for row in content:
        pseudocode = row[0]
        item_desc = row[1]
        
        # Accumulate the values for the current item_desc
        for i in range(2, len(row)):
            value = int(row[i])
            temp_item_desc[pseudocode][item_desc] += value

# Dictionary to hold the item descriptions with their accumulated values and counts (for 127_enr1.csv)
item_desc_values = defaultdict(list)

# Open and process 127_enr1.csv to calculate means and max values
with open("127_enr1.csv", "r", encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)  # Skip the header row
    
    # Collect all values for means calculation and max value determination
    for row in content:
        pseudocode = row[0]
        item_desc = row[1]
        
        # Accumulate the values for the current item_desc
        for i in range(2, len(row)):
            value = int(row[i])
            item_desc_values[item_desc].append(value)

# Calculate the mean for each item_desc from 127_enr1.csv
means = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values.items()}

# Calculate maximum values for normalization from 127_enr1.csv
max_values = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values.items()}

# Calculate Euclidean distance similarity using means for pseudocodes from 129_enr1.csv
similarities = {}

for pseudocode, items in temp_item_desc.items():
    distance = 0
    for item_desc, value in items.items():
        normalized_value = value / max_values[item_desc] if max_values[item_desc] != 0 else 0
        normalized_mean = means[item_desc] / max_values[item_desc] if max_values[item_desc] != 0 else 0
        distance += (normalized_value - normalized_mean) ** 2
    distance = math.sqrt(distance)
    similarity = 1 / (1 + distance)
    similarities[pseudocode] = similarity

# Output the corresponding information from 129_prof1.csv for pseudocodes with high similarity
threshold = 0.995  # Adjust the similarity threshold as needed
for pseudocode, similarity in similarities.items():
    if similarity > threshold:
        with open("129_prof1.csv", "r", encoding='utf-8') as file:
            content = csv.reader(file)
            header = next(content)  # Skip the header row
            for row in content:
                if pseudocode == row[0]:
                    print(row[2])  # Print the relevant information from 129_prof1.csv
                    
et = time.process_time()
print(et-st)
