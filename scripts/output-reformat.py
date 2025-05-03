import csv
import os
import re
from collections import defaultdict

def extract_date_from_path(file_path):
    """
    Extract the date from a quarterly version path.

    Args:
        file_path (str): The path to check (e.g., "versions/2017/Q1_2017-01-01/...")

    Returns:
        str: The date string (e.g., "2017-01-01") or None if not found
    """
    # Normalize path separators
    normalized_path = file_path.replace('\\', '/')

    # Look for quarterly version pattern (Q#_YYYY-MM-DD)
    match = re.search(r'Q\d+_(\d{4}-\d{2}-\d{2})', normalized_path)
    if match:
        return match.group(1)

    return None

def restructure_csv(input_file, output_file):
    """
    Restructure CSV by converting each 'Metric' value to a column,
    removing the 'Section' column, and keeping one row per file version.
    Also adds date extraction from filepath.
    """
    # Read the input CSV file
    rows_by_file = defaultdict(dict)
    metrics_set = set()

    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Group metrics by file
        for row in reader:
            # Skip rows with invalid data
            if not row.get('Filepath') or not row.get('Metric'):
                continue

            file_key = (row['Filepath'], row['Filename'], row.get('Version', ''))
            metric_name = row['Metric']
            metric_value = row['Value']

            # Store the metric value for this file
            rows_by_file[file_key][metric_name] = metric_value

            # Keep track of all unique metrics for headers
            if metric_name and metric_name != 'None':
                metrics_set.add(metric_name)

    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Sort metrics for consistent column order
    metrics_list = sorted(list(metrics_set))

    # Create the headers for the output CSV
    headers = ['Filepath', 'Filename', 'Version', 'Date'] + metrics_list

    # Write the restructured data to output file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        # Write each file's data as a single row
        for file_key, metrics in rows_by_file.items():
            filepath, filename, version = file_key

            # Extract date from filepath
            date = extract_date_from_path(filepath)

            # Start with the file identifiers
            row_data = {
                'Filepath': filepath,
                'Filename': filename,
                'Version': version,
                'Date': date or ''  # Use empty string if date is None
            }

            # Add all metrics for this file
            for metric in metrics_list:
                # Only include valid metrics (skip None)
                if metric and metric != 'None':
                    row_data[metric] = metrics.get(metric, '')

            writer.writerow(row_data)

    print(f"Restructured data written to {output_file}")
    print(f"Processed {len(rows_by_file)} unique files with {len(metrics_list)} metrics per file")

if __name__ == "__main__":
    input_file = "plotly/js/output-quarter.csv"
    output_file = "plotly/js/output-quarter-formatted.csv"

    restructure_csv(input_file, output_file)