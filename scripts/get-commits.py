import csv
import requests
import time
import concurrent.futures

output = 'plotly/js/commits.csv'
api_url = 'https://api.github.com/repos/plotly/plotly.js/commits'
# Github > Settings > Developer Settings > Personal access tokens > Generate new token
github_token = ""
if not github_token:
    print("GitHub token is required. Set GITHUB_TOKEN environment variable.")
    exit(1)
headers = {'Authorization': f'token {github_token}'}

def get_commit_details(sha):
    commit_url = f'{api_url}/{sha}'
    response = requests.get(commit_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Create/open CSV file for writing
with open(output, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Commit SHA', 'Author', 'Author Email', 'Date', 'Message', 'URL', 'Additions', 'Deletions', 'Total Changes'])

    page = 1
    total_commits = 0

    while True:
        # Fetch commits with pagination
        params = {'page': page, 'per_page': 100}
        response = requests.get(api_url, params=params, headers=headers)

        # Check remaining rate limit
        rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        print(f"Rate limit remaining: {rate_limit_remaining}")

        if response.status_code == 200:
            commits = response.json()

            if not commits:
                break  # No more commits, exit the loop

            # Fetch commit details in parallel (up to 10 concurrent requests)
            commit_shas = [commit['sha'] for commit in commits]
            commit_details = {}

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_sha = {executor.submit(get_commit_details, sha): sha for sha in commit_shas}
                for future in concurrent.futures.as_completed(future_to_sha):
                    sha = future_to_sha[future]
                    try:
                        data = future.result()
                        if data:
                            commit_details[sha] = data
                    except Exception as exc:
                        print(f"Error processing commit {sha}: {exc}")

            # Write commits to CSV
            for commit in commits:
                sha = commit.get('sha')
                commit_data = commit.get('commit', {})
                author = commit_data.get('author', {})

                additions = 0
                deletions = 0
                total_changes = 0

                if sha in commit_details:
                    detail_data = commit_details[sha]
                    stats = detail_data.get('stats', {})
                    additions = stats.get('additions', 0)
                    deletions = stats.get('deletions', 0)
                    total_changes = additions + deletions

                writer.writerow([
                    sha,
                    author.get('name'),
                    author.get('email'),
                    author.get('date'),
                    commit_data.get('message', '').strip().replace('\n', ' '),
                    commit.get('html_url'),
                    additions,
                    deletions,
                    total_changes
                ])

            total_commits += len(commits)
            print(f"Processed page {page} with {len(commits)} commits. Total: {total_commits}")
            page += 1  # Go to the next page

        elif response.status_code == 403 and 'rate limit' in response.text.lower():
            # Wait until rate limit reset
            reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
            wait_time = max(reset_time - time.time(), 0) + 10
            print(f"Rate limit reached. Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time)
            continue
        else:
            print(f"Failed to fetch commits. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            break

print(f"Commits exported to {output}")