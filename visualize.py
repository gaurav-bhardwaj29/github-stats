import matplotlib.pyplot as plt
from exporter import export_data

def plot_commit_activity(commit_activity, repo_name):
    weeks = list(range(1, len(commit_activity) + 1))
    commits = [week['total'] for week in commit_activity]
    plt.figure(figsize=(10, 4))
    plt.plot(weeks, commits, marker='o')
    plt.title(f"Weekly Commits for {repo_name}")
    plt.xlabel("Week (most recent = right)")
    plt.ylabel("Number of commits")
    plt.tight_layout()
    plt.show()
    export_data_option = input("Export this data? (csv/json/none): ").strip().lower()
    if export_data_option in ["csv", "json"]:
        export_data(commit_activity, f"{repo_name}_weekly_commits.{export_data_option}", export_data_option)

def plot_contributors(contributors, repo_name):
    top = sorted(contributors, key=lambda x: x['contributions'], reverse=True)[:10]
    names = [c['login'] for c in top]
    contribs = [c['contributions'] for c in top]
    plt.figure(figsize=(10, 5))
    plt.bar(names, contribs)
    plt.title(f"Top Contributors to {repo_name}")
    plt.ylabel("Contributions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    export_data_option = input("Export this data? (csv/json/none): ").strip().lower()
    if export_data_option in ["csv", "json"]:
        export_data(top, f"{repo_name}_top_contributors.{export_data_option}", export_data_option)