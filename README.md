# GitHub Repo Stats Dashboard
A simple Python script to fetch and display repository stats (stars, forks, open issues, watcher count, last created) using the GitHub API.

## How to Use
1. Install Python and the `requests` library (`pip install requests`).
2. Generate a GitHub fine-grained PAT with "Metadata: Read-only" (and optionally "Issues: Read-only") for public repos.
3. **Personal Use**: Replace `"your_personal_access_token"` in the script with your PAT.
   **Production Use**: Set the `GITHUB_TOKEN` environment variable (e.g., `export GITHUB_TOKEN=your_pat`) instead of hardcoding.
4. Run the script (`python repo_stats.py`) and enter a repository owner and name.

-----

## Features and Functionalities Added:

 - Web dashboard with a form for stats display, contributor lists, & commit activity
 - Visualization of commit activity and top contributors
 - Data export options (CSV/JSON)
