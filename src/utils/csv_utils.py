import csv
import statistics
from typing import Dict, List, Any

def read_csv_to_dict(file_path: str, key_col: int, value_cols: List[int]) -> Dict[Any, List[float]]:
    """
    Reads a CSV and returns a dictionary with key_col as key and list of values from value_cols.
    """
    result = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            key = row[key_col]
            values = []
            for idx in value_cols:
                try:
                    values.append(float(row[idx]))
                except (ValueError, IndexError):
                    continue
            if key in result:
                result[key].extend(values)
            else:
                result[key] = values
    return result

def calculate_means(data: Dict[Any, List[float]]) -> Dict[Any, float]:
    """
    Calculates the mean for each key in the dictionary.
    """
    return {k: statistics.mean(v) if v else 0 for k, v in data.items()}

def calculate_max_values(data: Dict[Any, List[float]]) -> Dict[Any, float]:
    """
    Calculates the max value for each key in the dictionary.
    """
    return {k: max(v) if v else 1 for k, v in data.items()}

def euclidean_similarity(vec1: Dict[Any, float], vec2: Dict[Any, float]) -> float:
    """
    Calculates the Euclidean similarity between two dictionaries (vectors).
    """
    keys = set(vec1.keys()) & set(vec2.keys())
    if not keys:
        return 0.0
    distance = sum((vec1[k] - vec2[k]) ** 2 for k in keys)
    return 1 / (1 + distance)

def normalize_dict(data: Dict[Any, float], max_values: Dict[Any, float]) -> Dict[Any, float]:
    """
    Normalizes the values in 'data' by dividing by corresponding values in 'max_values'.
    If max_value is 0, result is 0.
    """
    return {k: (v / max_values[k] if max_values.get(k, 0) != 0 else 0) for k, v in data.items()}

def write_dict_to_csv(data: Dict[Any, Any], file_path: str, header: List[str] = None):
    """
    Writes a dictionary to a CSV file. If header is provided, writes it as the first row.
    """
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        for k, v in data.items():
            if isinstance(v, (list, tuple)):
                writer.writerow([k] + list(v))
            else:
                writer.writerow([k, v])
