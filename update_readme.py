import os
from github import Github
from datetime import datetime, timedelta
import humanize

def update_readme():
    g = Github(os.environ['GITHUB_TOKEN'])

    # Read repositories from file
    with open('repositories.txt', 'r') as f:
        repos = [line.strip().split(',') for line in f]

    # Get repo information and sort by last commit date
    repo_info = []
    for repo_name, added_date in repos:
        repo = g.get_repo(repo_name)
        if repo:
            last_commit = repo.get_commits()[0].commit.author.date
            time_ago = humanize.naturaltime(datetime.now(last_commit.tzinfo) - last_commit)
            repo_info.append((repo, last_commit, time_ago, added_date))

    # Sort repos by last commit date, newest first
    repo_info.sort(key=lambda x: x[1], reverse=True)

    with open('README.md', 'w') as f:
        f.write("# Awesome Smart Contract Audits\n\n")
        f.write("This is a curated list of repositories containing smart contract audits. ")
        f.write("The list is automatically updated daily.\n\n")
        f.write("## Audit Repositories\n\n")
        f.write("| Repository | Description | Last Commit | Added On |\n")
        f.write("|------------|-------------|:-----------:|:--------:|\n")

        total_repos = 0
        newest_project = None
        one_month_ago = datetime.now() - timedelta(days=30)

        for repo, last_commit, time_ago, added_date in repo_info:
            total_repos += 1
            added_date_obj = datetime.strptime(added_date, '%Y-%m-%d')
            
            if not newest_project or added_date_obj > datetime.strptime(newest_project[1], '%Y-%m-%d'):
                newest_project = (repo.full_name, added_date)

            new_tag = " 🆕" if added_date_obj > one_month_ago else ""
            
            f.write(f"| [{repo.full_name}]({repo.html_url}){new_tag} | {repo.description or 'No description'} | {last_commit.strftime('%Y-%m-%d')} ({time_ago}) | {added_date} |\n")

        f.write("\n## Statistics\n\n")
        f.write(f"- Total number of audit repositories: {total_repos}\n")
        if newest_project:
            f.write(f"- Newest addition: [{newest_project[0]}](https://github.com/{newest_project[0]}) (added on {newest_project[1]})\n")

        f.write("\n## Contributing\n\n")
        f.write("To add a new audit repository to this list, please follow these steps:\n\n")
        f.write("1. Fork this repository\n")
        f.write("2. Edit the `repositories.txt` file in your fork, adding a new line with the format: `user/repo,YYYY-MM-DD`\n")
        f.write("   - `user/repo` is the GitHub username and repository name\n")
        f.write("   - `YYYY-MM-DD` is the date you're adding this repository to the list\n")
        f.write("3. Create a pull request with your changes\n")
        f.write("4. In the pull request description, please provide a brief explanation of why this repository should be included\n\n")
        f.write("Once your pull request is reviewed and merged, the README will be automatically updated to include the new repository.\n\n")

        f.write("## About Automatic Updates\n\n")
        f.write("This README file is automatically updated daily at midnight using GitHub Actions. ")
        f.write("This ensures you always have access to the most current information about these audit repositories.\n\n")
        f.write("## Contact\n\n")
        f.write("If you have any questions or suggestions, feel free to reach out:\n\n")
        f.write("- Twitter: [@yourusername](https://twitter.com/yourusername)\n\n")
        f.write(f"---\n\n*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n")

if __name__ == "__main__":
    update_readme()
