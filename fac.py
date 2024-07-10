import csv
from collections import defaultdict
import math
import statistics
from concurrent.futures import ThreadPoolExecutor
import time

# Dictionaries to hold the pseudocode and corresponding item descriptions with their accumulated values
temp_item_desc_1 = defaultdict(lambda: defaultdict(int))
temp_item_desc_2 = defaultdict(lambda: defaultdict(int))
temp_item_desc_fac = defaultdict(lambda: defaultdict(int))

# Dictionary to hold the item descriptions with their accumulated values and counts
item_desc_values_1 = defaultdict(list)
item_desc_values_2 = defaultdict(list)
item_desc_values_fac = defaultdict(list)

# Function to process 129_enr1.csv, 129_enr2.csv, and 129_fac.csv
def process_129_csv(file_name, temp_item_desc):
    try:
        with open(file_name, "r", encoding='utf-8') as file:
            content = csv.reader(file)
            next(content)  # Skip the header row
            for row in content:
                pseudocode = row[0]
                item_desc = row[1]
                for i in range(2, len(row)):
                    value = int(row[i])
                    temp_item_desc[pseudocode][item_desc] += value
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Function to process 127_enr1.csv, 127_enr2.csv, and 127_fac.csv
def process_127_csv(file_name, item_desc_values, is_fac=False):
    try:
        with open(file_name, "r", encoding='utf-8') as file:
            content = csv.reader(file)
            header = next(content)  # Read the header row
            if is_fac:
                headers = header[1:]  # Store column headers for 127_fac.csv
            for row in content:
                pseudocode = row[0]
                if is_fac:
                    for i in range(1, len(row)):
                        value = int(row[i])
                        item_desc_values[headers[i-1]].append(value)
                else:
                    item_desc = row[1]
                    for i in range(2, len(row)):
                        value = int(row[i])
                        item_desc_values[item_desc].append(value)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Function to calculate means and max values
def calculate_means_and_max_values(item_desc_values_1, item_desc_values_2, item_desc_values_fac):
    means_1 = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values_1.items()}
    means_2 = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values_2.items()}
    means_fac = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values_fac.items()}
    max_values_1 = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values_1.items()}
    max_values_2 = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values_2.items()}
    max_values_fac = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values_fac.items()}
    return means_1, means_2, means_fac, max_values_1, max_values_2, max_values_fac

# Function to calculate similarities
def calculate_similarities(temp_item_desc, means, max_values):
    similarities = {}
    for pseudocode, items in temp_item_desc.items():
        distance = 0
        for item_desc, value in items.items():
            try:
                if item_desc not in max_values:
                    raise KeyError(f"{item_desc} not found in max_values")
                normalized_value = value / max_values[item_desc] if max_values[item_desc] != 0 else 0
                normalized_mean = means[item_desc] / max_values[item_desc] if max_values[item_desc] != 0 else 0
                distance += (normalized_value - normalized_mean) ** 2
            except KeyError as e:
                #print(f"KeyError: {e}")
                continue
        distance = math.sqrt(distance)
        similarity = 1 / (1 + distance)
        similarities[pseudocode] = similarity
    return similarities

# Function to output information from 129_prof1.csv based on similarities in both cases
def output_high_similarity_info(similarities_1, similarities_2, similarities_fac, threshold=0.99):
    unique_outputs = set()
    with open("129_prof1.csv", "r", encoding='utf-8') as file:
        content = csv.reader(file)
        next(content)  # Skip the header row
        for row in content:
            pseudocode = row[0]
            if (pseudocode in similarities_1 and similarities_1[pseudocode] > threshold) and \
               (pseudocode in similarities_2 and similarities_2[pseudocode] > threshold) and \
               (pseudocode in similarities_fac and similarities_fac[pseudocode] > threshold):
                unique_outputs.add(row[2])  # Add the relevant information to the set

    for output in unique_outputs:
        print(output)  # Print unique outputs

# Main function to run all tasks
def main():
    start_time = time.time()  # Record start time

    with ThreadPoolExecutor() as executor:
        # Process 129_enr1.csv, 129_enr2.csv, and 129_fac.csv
        executor.submit(process_129_csv, "129_enr1.csv", temp_item_desc_1)
        executor.submit(process_129_csv, "129_enr2.csv", temp_item_desc_2)
        executor.submit(process_129_csv, "129_fac.csv", temp_item_desc_fac)
        
        # Process 127_enr1.csv, 127_enr2.csv, and 127_fac.csv
        executor.submit(process_127_csv, "127_enr1.csv", item_desc_values_1)
        executor.submit(process_127_csv, "127_enr2.csv", item_desc_values_2)
        executor.submit(process_127_csv, "127_fac.csv", item_desc_values_fac, is_fac=True)

    # Calculate means and max values
    means_1, means_2, means_fac, max_values_1, max_values_2, max_values_fac = calculate_means_and_max_values(item_desc_values_1, item_desc_values_2, item_desc_values_fac)

    # Calculate similarities for all sets
    similarities_1 = calculate_similarities(temp_item_desc_1, means_1, max_values_1)
    similarities_2 = calculate_similarities(temp_item_desc_2, means_2, max_values_2)
    similarities_fac = calculate_similarities(temp_item_desc_fac, means_fac, max_values_fac)

    # Output high similarity information for all sets
    output_high_similarity_info(similarities_1, similarities_2, similarities_fac)

    end_time = time.time()  # Record end time
    print(f"Total runtime: {end_time - start_time:.2f} seconds")  # Print the total runtime

if __name__ == "__main__":
    main()

