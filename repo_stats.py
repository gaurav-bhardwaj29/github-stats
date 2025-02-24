import requests
import os

def get_repo_stats(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        open_issues = data.get("open_issues_count", 0)
        return stars, forks, open_issues
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    owner = input("Enter the repository owner: ")
    repo = input("Enter the repository name: ")
    
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        # token = "your_personal_access_token"  # Replace this for personal use
        print("No GITHUB_TOKEN found in environment. Falling back >>")
        token = input("Enter your GitHub token: ")
    
    stats = get_repo_stats(owner, repo, token)
    if stats:
        stars, forks, open_issues = stats
        print(f"\nRepository: {owner}/{repo}")
        print(f"Stars: {stars}")
        print(f"Forks: {forks}")
        print(f"Open Issues: {open_issues}")
    else:
        print("Failed to fetch repository stats.")
