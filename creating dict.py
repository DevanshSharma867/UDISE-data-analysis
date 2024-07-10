import csv

# Dictionary to hold the pseudocode and corresponding item descriptions with their accumulated values
temp_item_desc = {}

# Open the CSV file
with open("127_enr1.csv", "r", encoding='utf-8') as file:
    content = csv.reader(file)
    header = next(content)  # Skip the header row
    
    # Process each row in the CSV
    for row in content:
        pseudocode = row[0]
        item_desc = row[1]
        
        # Initialize the pseudocode entry if it does not exist
        if pseudocode not in temp_item_desc:
            temp_item_desc[pseudocode] = {}
        
        # Initialize the item_desc entry if it does not exist
        if item_desc not in temp_item_desc[pseudocode]:
            temp_item_desc[pseudocode][item_desc] = 0
        
        # Accumulate the values for the current item_desc
        for i in range(2, len(row)):
            temp_item_desc[pseudocode][item_desc] += int(row[i])

# Print the resulting dictionary
print(temp_item_desc)
