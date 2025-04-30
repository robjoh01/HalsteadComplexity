import csv
import datetime

input_file = "plotly/python/commits.csv"
output_file = "plotly/python/commits-sorted.csv"

# Read the CSV file
with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Parse the date strings into datetime objects for sorting
for row in rows:
    # Convert ISO format date string to datetime object
    row['datetime_obj'] = datetime.datetime.fromisoformat(row['Date'].replace('Z', '+00:00'))

# Sort rows by date (newest first)
sorted_rows = sorted(rows, key=lambda x: x['datetime_obj'], reverse=True)

# Remove the temporary datetime objects used for sorting
for row in sorted_rows:
    del row['datetime_obj']

# Write the sorted data to the output file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    # Use the same fieldnames from the original file
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(sorted_rows)

print(f"Sorted commits by date (newest first) and saved to {output_file}")