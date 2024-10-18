import os
import re
from github import Github
from datetime import datetime, timedelta

def extract_twitter_username(text):
    twitter_pattern = r'(?:https?://)?(?:www\.)?(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+)'
    match = re.search(twitter_pattern, text)
    return match.group(1) if match else None

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
            stars = repo.stargazers_count
            twitter_user = extract_twitter_username(repo.description or "")
            followers = repo.organization.followers_count if repo.organization else "N/A"

            # Extract Twitter username from organization description if available
            if repo.organization:
                twitter_user_org = extract_twitter_username(repo.organization.description or "")
                twitter_user = twitter_user or twitter_user_org
            
            repo_info.append((repo, last_commit, added_date, stars, twitter_user, followers))

    # Sort repos by last commit date, newest first
    repo_info.sort(key=lambda x: x[1], reverse=True)

    with open('README.md', 'w') as f:
        f.write("# Awesome Smart Contract Audits\n\n")
        f.write("This is a curated list of repositories containing smart contract audits. ")
        f.write("The list is automatically updated daily.\n\n")
        f.write("## Audit Repositories\n\n")
        f.write("| Repository | Description | Last Commit | Added On | Stars & Followers | Twitter |\n")
        f.write("|------------|-------------|:-----------:|:--------:|:------------------:|---------|\n")

        for repo, last_commit, added_date, stars, twitter_user, followers in repo_info:
            twitter_link = f"[{twitter_user}](https://twitter.com/{twitter_user})" if twitter_user else "N/A"
            f.write(f"| [{repo.full_name}]({repo.html_url}) | {repo.description or 'No description'} | {last_commit.strftime('%Y-%m-%d')} | {added_date} | {stars} / {followers} | {twitter_link} |\n")

        f.write("\n## Legend\n\n")
        f.write("* 🆕: New repository (added in the last month)\n")
        f.write("* 😴: Sleepy repository (last commit over six months ago)\n")
        f.write("\n## Statistics\n\n")
        f.write(f"- Total number of audit repositories: {len(repo_info)}\n")

if __name__ == "__main__":
    update_readme()
