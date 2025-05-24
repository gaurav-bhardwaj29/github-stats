import sys

def handle_github_error(resp):
    if resp.status_code == 403:
        print("Error: Rate limit exceeded or invalid token. Please check your GitHub token and try again.")
        sys.exit(1)
    elif resp.status_code == 404:
        print("Error: Repository not found. Please check the owner/repo name.")
        sys.exit(1)
    elif resp.status_code == 401:
        print("Error: Unauthorized. Invalid or missing token.")
        sys.exit(1)
    else:
        print(f"Unexpected error from GitHub API: {resp.status_code} {resp.text}")
        sys.exit(1)