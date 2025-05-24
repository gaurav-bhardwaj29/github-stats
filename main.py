import os
from insights import get_repo_stats, get_pr_stats, get_contributors, get_commit_activity
from visualize import plot_commit_activity, plot_contributors
from exporter import export_data

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        token = input("Enter your GitHub token: ").strip()
    return token

def main():
    owner = input("Repository owner: ").strip()
    repo = input("Repository name: ").strip()
    token = get_token()

    print("\nFetching enhanced repository insights...\n")
    try:
        basic_stats = get_repo_stats(owner, repo, token)
        
        pr_count = get_pr_stats(owner, repo, token)
        contributors = get_contributors(owner, repo, token)
        commit_activity = get_commit_activity(owner, repo, token)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return
    basic_stats = get_repo_stats(owner, repo, token)
    print("\nRepository Stats:")
    for k, v in basic_stats.items():
        print(f"  {k.replace('_', ' ').title()}: {v}")
    print(f"PRs (all): {pr_count}")
    print(f"Contributors: {len(contributors)}")
    print("Top 5 contributors:")
    for c in sorted(contributors, key=lambda x: x['contributions'], reverse=True)[:5]:
        print(f"  {c['login']}: {c['contributions']}")

    print("\nVisualization options:")
    print("1. Plot weekly commit activity")
    print("2. Plot top contributors")
    print("3. Export all data")
    print("4. Exit")

    while True:
        choice = input("\nChoose an option (1-4): ").strip()
        if choice == "1":
            plot_commit_activity(commit_activity, repo)
        elif choice == "2":
            plot_contributors(contributors, repo)
        elif choice == "3":
            export_format = input("Export format (csv/json): ").strip().lower()
            if export_format not in ["csv", "json"]:
                print("Invalid format.")
                continue
            export_data({
                "pr_count": pr_count,
                "contributors": contributors,
                "commit_activity": commit_activity
            }, f"{repo}_all_data.{export_format}", export_format)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()