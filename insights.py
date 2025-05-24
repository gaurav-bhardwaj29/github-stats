import requests
from utils import handle_github_error
import time

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
        return {
            "stars": stars,
            "forks": forks,
            "open_issues": open_issues,
            "watchers": watchers,
            "last_updated": last_updated
        }
    else:
        handle_github_error(response)

def get_pr_stats(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=all&per_page=1"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        handle_github_error(resp)
    if "Link" in resp.headers:
        link = resp.headers["Link"]
        import re
        match = re.search(r'&page=(\d+)>; rel="last"', link)
        if match:
            total_prs = int(match.group(1))
        else:
            total_prs = len(resp.json())
    else:
        total_prs = len(resp.json())
    return total_prs

def get_contributors(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100"
    headers = {"Authorization": f"Bearer {token}"}
    contributors = []
    page = 1
    while True:
        resp = requests.get(url + f"&page={page}", headers=headers)
        if resp.status_code != 200:
            handle_github_error(resp)
        data = resp.json()
        if not data:
            break
        contributors.extend(data)
        page += 1
    return [{"login": c["login"], "contributions": c["contributions"]} for c in contributors]

def get_commit_activity(owner, repo, token, retries=5, wait=2):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity"
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(retries):
        resp = requests.get(url, headers=headers)
        if resp.status_code == 202:
            print("GitHub is generating commit activity data, waiting a few seconds...")
            time.sleep(wait)
            continue
        elif resp.status_code != 200:
            handle_github_error(resp)
        weekly_data = resp.json()
        if not isinstance(weekly_data, list):
            print("Unexpected data format from GitHub API.")
            return []
        return weekly_data
    print("GitHub did not return commit activity data in time. Please try again later.")
    return []

if __name__ == "__main__":
    import os
    owner = input("Repository owner: ")
    repo = input("Repository name: ")
    token = os.environ.get("GITHUB_TOKEN") or input("GitHub Token: ")
    basic_stats = get_repo_stats(owner, repo, token)
    print("Basic repository stats:")
    for k, v in basic_stats.items():
        print(f"  {k}: {v}")
    print(f"Total PRs: {get_pr_stats(owner, repo, token)}")
    contributors = get_contributors(owner, repo, token)
    print(f"Total contributors: {len(contributors)}")
    top = sorted(contributors, key=lambda x: x['contributions'], reverse=True)[:5]
    print("Top 5 contributors:")
    for c in top:
        print(f"  {c['login']}: {c['contributions']} commits")
    commits = get_commit_activity(owner, repo, token)
    print(f"Weekly commit activity for last {len(commits)} weeks available.")
