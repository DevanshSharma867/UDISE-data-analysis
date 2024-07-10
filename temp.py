import csv
from collections import defaultdict
import math
import statistics

# Function to calculate similarities between two sets of files
def calculate_similarity(file1, file2):
    # Dictionary to hold the pseudocode and corresponding item descriptions with their accumulated values
    temp_item_desc = defaultdict(lambda: defaultdict(int))

    # Open and process file1
    with open(file1, "r", encoding='utf-8') as file:
        content = csv.reader(file)
        header = next(content)  # Skip the header row
        
        # Process each row in the CSV for pseudocodes from file1
        for row in content:
            pseudocode = row[0]
            item_desc = row[1]
            
            # Accumulate the values for the current item_desc
            for i in range(2, len(row)):
                value = int(row[i])
                temp_item_desc[pseudocode][item_desc] += value

    # Dictionary to hold the item descriptions with their accumulated values and counts (for file2)
    item_desc_values = defaultdict(list)

    # Open and process file2 to calculate means and max values
    with open(file2, "r", encoding='utf-8') as file:
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

    # Calculate the mean for each item_desc from file2
    means = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values.items()}

    # Calculate maximum values for normalization from file2
    max_values = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values.items()}

    # Calculate Euclidean distance similarity using means for pseudocodes from file1
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

    return similarities

# Main script execution
if __name__ == "__main__":
    # File paths
    file127_enr1 = "127_enr1.csv"
    file127_enr2 = "127_enr2.csv"
    file129_enr1 = "129_enr1.csv"
    file129_enr2 = "129_enr2.csv"
    file129_prof1 = "129_prof1.csv"

    # Calculate similarities for initial files
    similarities_initial = calculate_similarity(file127_enr1, file129_enr1)

    # Calculate similarities for additional files
    similarities_additional = calculate_similarity(file127_enr2, file129_enr2)

    # Output the combined similarities
    for pseudocode in similarities_initial:
        similarity_initial = similarities_initial.get(pseudocode, 0)
        similarity_additional = similarities_additional.get(pseudocode, 0)
        
        # Print the combined similarity results
        # print(f"{pseudocode}: Similarity between initial files - {similarity_initial:.4f}, Similarity between additional files - {similarity_additional:.4f}")

        # Optionally, print the corresponding information from 129_prof1.csv for pseudocodes with high similarity
        threshold = 0.99  # Adjust the similarity threshold as needed
        if similarity_initial > threshold or similarity_additional > threshold:
            with open(file129_prof1, "r", encoding='utf-8') as file:
                content = csv.reader(file)
                header = next(content)  # Skip the header row
                for row in content:
                    if pseudocode == row[0]:
                        print(f"   - {row[2]}")  # Print the relevant information from 129_prof1.csv
