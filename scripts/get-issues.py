import csv
import requests

output = 'plotly/js/issues.csv'
api_url = 'https://api.github.com/repos/plotly/plotly.js/issues'

# Create a CSV file with UTF-8 encoding
with open(output, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Number', 'Title', 'State', 'Created At', 'Updated At', 'Assignee', 'Labels'])

    page = 1
    while True:
        # Fetch issues with pagination
        params = {'labels': 'bug', 'state': 'all', 'page': page, 'per_page': 100}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            issues = response.json()

            if not issues:
                break  # No more issues, exit the loop

            # Write issues to CSV
            for issue in issues:
                writer.writerow([
                    issue.get('number'),
                    issue.get('title'),
                    issue.get('state'),
                    issue.get('created_at'),
                    issue.get('updated_at'),
                    issue.get('assignee')['login'] if issue.get('assignee') else None,
                    ", ".join([label['name'] for label in issue.get('labels', [])])
                ])

            page += 1  # Go to the next page
        else:
            print("Failed to fetch issues. Status code:", response.status_code)
            break

print(f"Issues exported to {output}")