import os
import re
import glob

def main():
    # Base directory
    base = os.path.abspath(os.getcwd())  # Current working directory

    # Directory pattern to match quarterly versions
    version_pattern = "plotly/js/versions/*/Q*_*"

    # Define directories to exclude
    exclude_dirs = ["dist", "specs", "test", "tests", "doc", "validators", "codegen"]

    # Output file
    output_file = "plotly/js/inputs-quarter.txt"

    # Find all version directories using glob
    version_dirs = glob.glob(version_pattern)

    # Sort the directories by date embedded in the directory name
    def get_date_from_dir(dir_path):
        # Extract date from pattern like "Q1_2017-01-01"
        match = re.search(r'Q\d+_(\d{4}-\d{2}-\d{2})', dir_path)
        if match:
            return match.group(1)
        return "0000-00-00"  # Default for sorting if no date found

    version_dirs.sort(key=get_date_from_dir)

    # Initialize lines array for output
    lines = []

    # Process each version directory
    for version_dir in version_dirs:
        print(f"Processing: {version_dir}")

        # Find all JavaScript files in this version directory
        js_files = []
        for root, dirs, files in os.walk(version_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            # Add JavaScript files
            for file in files:
                if file.endswith(".js"):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base)
                    js_files.append(relative_path)

        # Add all files from this version to the output
        lines.extend(js_files)
        # Add an empty line between versions
        lines.append("")

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the results to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Processing complete. Results written to {output_file}")
    print(f"Processed {len(version_dirs)} version directories.")

if __name__ == "__main__":
    main()