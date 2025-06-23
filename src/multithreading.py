import csv
from collections import defaultdict
import math
import statistics
from concurrent.futures import ThreadPoolExecutor
import time

# Dictionary to hold the pseudocode and corresponding item descriptions with their accumulated values (for 129_enr1.csv)
temp_item_desc = defaultdict(lambda: defaultdict(int))

# Dictionary to hold the item descriptions with their accumulated values and counts (for 127_enr1.csv)
item_desc_values = defaultdict(list)

# Function to process 129_enr1.csv and 127_enr1.csv in parallel
def process_csv(file_name, process_129):
    if process_129:
        with open(file_name, "r", encoding='utf-8') as file:
            content = csv.reader(file)
            next(content)  # Skip the header row
            for row in content:
                pseudocode = row[0]
                item_desc = row[1]
                for i in range(2, len(row)):
                    value = int(row[i])
                    temp_item_desc[pseudocode][item_desc] += value
    else:
        with open(file_name, "r", encoding='utf-8') as file:
            content = csv.reader(file)
            next(content)  # Skip the header row
            for row in content:
                item_desc = row[1]
                for i in range(2, len(row)):
                    value = int(row[i])
                    item_desc_values[item_desc].append(value)

# Function to calculate means and max values
def calculate_means_and_max_values():
    means = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values.items()}
    max_values = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values.items()}
    return means, max_values

# Function to calculate similarities
def calculate_similarities(means, max_values):
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

# Function to output information from 129_prof1.csv based on similarities
def output_high_similarity_info(similarities, threshold=0.995):
    with open("129_prof1.csv", "r", encoding='utf-8') as file:
        content = csv.reader(file)
        next(content)  # Skip the header row
        for row in content:
            pseudocode = row[0]
            if pseudocode in similarities and similarities[pseudocode] > threshold:
                print(row[2])  # Print the relevant information from 129_prof1.csv

# Main function to run all tasks
def main():
    start_time = time.time()  # Record start time

    with ThreadPoolExecutor() as executor:
        executor.submit(process_csv, "129_enr1.csv", True)
        executor.submit(process_csv, "127_enr1.csv", False)

    means, max_values = calculate_means_and_max_values()
    similarities = calculate_similarities(means, max_values)
    output_high_similarity_info(similarities)

    end_time = time.time()  # Record end time
    print(f"Total runtime: {end_time - start_time:.2f} seconds")  # Print the total runtime

if __name__ == "__main__":
    main()

