import requests
import os
from datetime import datetime

def get_repo_stats(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        open_issues = data.get("open_issues_count", 0)
        watchers = data.get("subscribers_count", 0)
        last_updated = data.get("pushed_at", "N/A")
        if last_updated != "N/A":
            last_updated = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M UTC")
        return stars, forks, open_issues, watchers, last_updated
    elif response.status_code == 404:
        return "Not found"
    elif response.status_code == 403:
        return "Rate limit exceeded"
    else:
        return f"Error: {response.status_code}"
def process_repos(repo_input, token):
    repos = [r.strip() for r in repo_input.split(",")]
    results = []
    
    for repo_str in repos:
        try:
            owner, repo = repo_str.split("/")
            stats = get_repo_stats(owner, repo, token)
            results.append((f"{owner}/{repo}", stats))
        except ValueError:
            results.append((repo_str, "Invalid format - use owner/repo"))
    
    return results

if __name__ == "__main__":
    print("Enter repositories (e.g., torvalds/linux)")
    repo_input = input("> ")
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        # token = "your_personal_access_token"  # Replace this for personal use
        print("No GITHUB_TOKEN found in environment. Falling back >>")
        token = input("Enter your GitHub token: ")
    
    if not repo_input:
        print("No repositories entered.")
    else:
        results = process_repos(repo_input, token)
        print("\nRepository Stats:")
        print("-" * 50)
        for repo, stats in results:
            if isinstance(stats, tuple):
                stars, forks, open_issues, watchers, last_updated = stats
                print(f"{repo}:")
                print(f"  Stars: {stars}")
                print(f"  Forks: {forks}")
                print(f"  Open Issues: {open_issues}")
                print(f"  Watchers: {watchers}")
                print(f"  Last Updated: {last_updated}")
            else:
                print(f"{repo}: {stats}")
            print("-" * 50)
