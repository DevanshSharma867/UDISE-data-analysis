import csv
import math
import statistics
from collections import defaultdict
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

# Function to process CSV files
def process_csv(file_name, temp_item_desc, item_desc_values=None, is_fac=False):
    try:
        with open(file_name, "r", encoding='utf-8') as file:
            content = csv.reader(file)
            header = next(content)  # Read the header row
            headers = header[1:] if is_fac else None
            for row in content:
                pseudocode = row[0]
                if is_fac:
                    for i, value in enumerate(row[1:], start=1):
                        item_desc_values[headers[i-1]].append(int(value))
                else:
                    item_desc = row[1]
                    for i, value in enumerate(row[2:], start=2):
                        temp_item_desc[pseudocode][item_desc] += int(value)
                        if not is_fac:
                            item_desc_values[item_desc].append(int(value))
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# Function to calculate means and max values
def calculate_means_and_max_values(item_desc_values):
    means = {item_desc: statistics.mean(values) if values else 0 for item_desc, values in item_desc_values.items()}
    max_values = {item_desc: max(values) if values else 1 for item_desc, values in item_desc_values.items()}
    return means, max_values

# Function to calculate similarities
def calculate_similarities(temp_item_desc, means, max_values):
    similarities = {}
    for pseudocode, items in temp_item_desc.items():
        distance = sum((value / max_values[item_desc] - means[item_desc] / max_values[item_desc]) ** 2
                       for item_desc, value in items.items() if item_desc in max_values)
        similarity = 1 / (1 + math.sqrt(distance))
        similarities[pseudocode] = similarity
    return similarities

# Function to output information based on similarities
def output_high_similarity_info(similarities, threshold=0.995):
    unique_outputs = set()
    with open("129_prof1.csv", "r", encoding='utf-8') as file:
        content = csv.reader(file)
        next(content)  # Skip the header row
        for row in content:
            pseudocode = row[0]
            if pseudocode in similarities and similarities[pseudocode] > threshold:
                unique_outputs.add(row[2])  # Add the relevant information to the set
    return unique_outputs

# Main function to run all tasks
def main():
    start_time = time.time()  # Record start time

    with ThreadPoolExecutor() as executor:
        # Process 129_enr1.csv, 129_enr2.csv, and 129_fac.csv
        executor.submit(process_csv, "129_enr1.csv", temp_item_desc_1)
        executor.submit(process_csv, "129_enr2.csv", temp_item_desc_2)
        executor.submit(process_csv, "129_fac.csv", temp_item_desc_fac)

        # Process 127_enr1.csv, 127_enr2.csv, and 127_fac.csv
        executor.submit(process_csv, "127_enr1.csv", temp_item_desc_1, item_desc_values_1)
        executor.submit(process_csv, "127_enr2.csv", temp_item_desc_2, item_desc_values_2)
        executor.submit(process_csv, "127_fac.csv", temp_item_desc_fac, item_desc_values_fac, True)

    # Calculate means and max values
    means_1, max_values_1 = calculate_means_and_max_values(item_desc_values_1)
    means_2, max_values_2 = calculate_means_and_max_values(item_desc_values_2)
    means_fac, max_values_fac = calculate_means_and_max_values(item_desc_values_fac)

    # Calculate similarities for all sets
    similarities_1 = calculate_similarities(temp_item_desc_1, means_1, max_values_1)
    similarities_2 = calculate_similarities(temp_item_desc_2, means_2, max_values_2)
    similarities_fac = calculate_similarities(temp_item_desc_fac, means_fac, max_values_fac)

    # Output high similarity information for all sets
    results = output_high_similarity_info(similarities_1, similarities_2, similarities_fac)

    # Append results to the CSV file
    with open("selected_districts.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for output in results:
            writer.writerow([output])

    end_time = time.time()  # Record end time
    print(f"Total runtime: {end_time - start_time:.2f} seconds")  # Print the total runtime

if __name__ == "__main__":
    main()
