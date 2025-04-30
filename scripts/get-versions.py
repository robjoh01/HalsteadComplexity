import csv
import os
import subprocess
import datetime
from collections import defaultdict

def read_commits_csv(csv_file_path):
    """Read the commits CSV file and return a list of commit dictionaries."""
    commits = []
    with open(csv_file_path, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert the date string to a datetime object
            date_str = row['Date']
            date_obj = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))

            # Add the datetime object to the row dictionary
            row['date_obj'] = date_obj
            commits.append(row)

    # Sort commits by date (oldest first)
    commits.sort(key=lambda x: x['date_obj'])
    return commits

def group_commits_by_quarter(commits):
    """Group commits by year and quarter."""
    quarterly_commits = defaultdict(list)

    for commit in commits:
        date_obj = commit['date_obj']
        year = date_obj.year
        quarter = (date_obj.month - 1) // 3 + 1  # Calculate quarter (1-4)

        key = (year, quarter)
        quarterly_commits[key].append(commit)

    return quarterly_commits

def get_first_commit_per_quarter(quarterly_commits):
    """Get the first commit from each quarter."""
    first_commits = {}

    for (year, quarter), commits in quarterly_commits.items():
        if commits:  # Ensure there's at least one commit
            first_commits[(year, quarter)] = commits[0]

    return first_commits

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def fetch_repository_version(commit_sha, output_dir):
    """Clone specific version of the repository based on the commit SHA."""
    repo_url = "https://github.com/plotly/plotly.py.git"

    # Create the output directory
    create_directory(output_dir)

    # Change to the output directory
    original_dir = os.getcwd()
    os.chdir(output_dir)

    try:
        # Initialize a new git repository
        subprocess.run(["git", "init"], check=True)

        # Add the remote repository
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

        # Fetch the specific commit
        subprocess.run(["git", "fetch", "--depth", "1", "origin", commit_sha], check=True)

        # Checkout the commit
        subprocess.run(["git", "checkout", commit_sha], check=True)

        print(f"Successfully fetched commit {commit_sha} to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching commit {commit_sha}: {e}")
    finally:
        # Return to the original directory
        os.chdir(original_dir)

def main():
    # CSV file path
    csv_file_path = "plotly/python/commits-sorted.csv"

    # Base directory for versions
    base_dir = "plotly/python/versions"

    # Read commits from CSV
    commits = read_commits_csv(csv_file_path)

    # Group commits by quarter
    quarterly_commits = group_commits_by_quarter(commits)

    # Get first commit per quarter
    first_commits = get_first_commit_per_quarter(quarterly_commits)

    # Process each year starting from 2017
    start_year = 2017
    current_year = datetime.datetime.now().year

    for year in range(start_year, current_year + 1):
        for quarter in range(1, 5):
            if (year, quarter) in first_commits:
                commit = first_commits[(year, quarter)]
                commit_sha = commit['Commit SHA']
                commit_date = commit['date_obj'].strftime('%Y-%m-%d')

                # Create year-specific directory
                year_dir = os.path.join(base_dir, str(year))

                # Create output directory with quarter and date info
                output_dir = os.path.join(year_dir, f"Q{quarter}_{commit_date}")

                # Fetch the repository version
                fetch_repository_version(commit_sha, output_dir)

if __name__ == "__main__":
    main()