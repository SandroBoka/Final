import os
import pandas as pd


def ensure_csv_directory():
    """Ensure that the csv_data directory exists."""
    csv_dir = "csv_data"
    os.makedirs(csv_dir, exist_ok=True)
    return csv_dir


def save_to_csv(filename, data, columns):
    """Save the given data to a CSV file in the csv_data directory."""
    csv_dir = ensure_csv_directory()
    df = pd.DataFrame(data, columns=columns)
    filepath = os.path.join(csv_dir, filename)
    df.to_csv(filepath, index=False)
