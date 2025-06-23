import csv
from collections import defaultdict

# Dictionary to hold the pseudocode and corresponding item descriptions with their accumulated values
temp_item_desc = defaultdict(lambda: defaultdict(int))
# Dictionary to hold the item descriptions with their accumulated values and counts
item_desc_totals = defaultdict(lambda: {'total': 0, 'count': 0})

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
            item_desc_totals[item_desc]['total'] += value
            item_desc_totals[item_desc]['count'] += 1

# Calculate the average for each item_desc
averages = {}
for item_desc, values in item_desc_totals.items():
    total = values['total']
    count = values['count']
    average = total / count if count != 0 else 0
    averages[item_desc] = average

# Function to calculate percentage similarity
def calculate_similarity(value, average):
    if average == 0:
        return 0.0
    return ((value - average) / average) * 100

# Calculate the net similarity for each pseudocode
net_similarity = {}
for pseudocode, items in temp_item_desc.items():
    total_similarity = 0
    count = 0
    for item_desc, total in items.items():
        average = averages.get(item_desc, 0)
        similarity = calculate_similarity(total, average)
        total_similarity += similarity
        count += 1
    net_similarity[pseudocode] = total_similarity / count if count != 0 else 0

# Print the resulting net similarities
for pseudocode, similarity in net_similarity.items():
    print(f"Pseudocode: {pseudocode}, Net Similarity: {similarity:.2f}%")
