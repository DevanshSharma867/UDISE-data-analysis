import csv
from collections import defaultdict
import math
import statistics

# Dictionary to hold the pseudocode and corresponding item descriptions with their accumulated values
temp_item_desc = defaultdict(lambda: defaultdict(int))
# Dictionary to hold the item descriptions with their accumulated values and counts
item_desc_values = defaultdict(list)

# Open the CSV file
with open("127_enr1.csv", "r", encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)  # Skip the header row
    
    # Process each row in the CSV
    for row in content:
        pseudocode = row[0]
        item_desc = row[1]
        
        # Accumulate the values for the current item_desc
        for i in range(2, len(row)):
            value = int(row[i])
            temp_item_desc[pseudocode][item_desc] += value
            item_desc_values[item_desc].append(value)

# Calculate the mean for each item_desc
means = {}
for item_desc, values in item_desc_values.items():
    means[item_desc] = statistics.mean(values) if values else 0
print(means)
# Normalize the item descriptions by dividing by the maximum value
max_values = {item_desc: max(item_desc_values[item_desc]) if item_desc_values[item_desc] else 1 for item_desc in item_desc_values}
print(max_values)
# Calculate Euclidean distance similarity using means
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


temp = 0
# Print the resulting similarities
for pseudocode, similarity in similarities.items():
    if similarity * 100 > 99.7:
        temp +=1
    # print(f"{pseudocode}: {similarity * 100}")
print(temp)