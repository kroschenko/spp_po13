from datetime import datetime, timedelta

import requests


def get_data(url):
    response = requests.get(
        url,
        timeout=10,
        headers={"Accept": "application/vnd.github+json"},
    )

    return response.json()


repository = input("Введите репозиторий (owner/repo): ")

hours = int(input("Введите диапазон времени в часах: "))

time_limit = datetime.utcnow() - timedelta(hours=hours)

base_url = f"https://api.github.com/repos/{repository}"

commits = get_data(f"{base_url}/commits")
issues = get_data(f"{base_url}/issues")
pulls = get_data(f"{base_url}/pulls")
repo_info = get_data(base_url)

new_commits = 0

for commit in commits:
    commit_date = datetime.strptime(
        commit["commit"]["author"]["date"],
        "%Y-%m-%dT%H:%M:%SZ",
    )

    if commit_date > time_limit:
        new_commits += 1

open_issues = 0
closed_issues = 0

for issue in issues:
    if "pull_request" not in issue:
        if issue["state"] == "open":
            open_issues += 1
        else:
            closed_issues += 1

open_pulls = 0
closed_pulls = 0

for pull in pulls:
    if pull["state"] == "open":
        open_pulls += 1
    else:
        closed_pulls += 1

print("\nМониторинг репозитория")
print(f"Коммитов: {new_commits}")
print(f"Открытых issues: {open_issues}")
print(f"Закрытых issues: {closed_issues}")
print(f"Открытых pull requests: {open_pulls}")
print(f"Закрытых pull requests: {closed_pulls}")
print(f"Звезды: {repo_info['stargazers_count']}")
print(f"Форки: {repo_info['forks_count']}")
