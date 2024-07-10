import csv
from collections import defaultdict

# Dictionary to hold the item descriptions with their accumulated values and counts
item_desc_totals = defaultdict(lambda: {'total': 0, 'count': 0})

# Open the CSV file
with open("127_enr1.csv", "r", encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)  # Skip the header row
    
    # Process each row in the CSV
    for row in content:
        item_desc = row[1]
        
        # Accumulate the values for the current item_desc and increment the count
        for i in range(2, len(row)):
            item_desc_totals[item_desc]['total'] += int(row[i])
            item_desc_totals[item_desc]['count'] += 1

# Calculate the average for each item_desc
averages = {}
for item_desc, values in item_desc_totals.items():
    total = values['total']
    count = values['count']
    average = total / count if count != 0 else 0
    averages[item_desc] = average

# Print the resulting averages
for item_desc, avg in averages.items():
    print(f"{item_desc}: {avg}")
