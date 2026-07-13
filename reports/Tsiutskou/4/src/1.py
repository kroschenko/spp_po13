import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

TOKEN = "YOUR_TOKEN_HERE"


def get_top_contributors(repo, days, min_commits):
    since = (datetime.now() - timedelta(days=days)).isoformat()

    headers = {"User-Agent": "Mozilla/5.0", "Authorization": f"token {TOKEN}"}

    url = f"https://api.github.com/repos/{repo}/contributors"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    contributors = response.json()
    result = []

    for c in contributors[:20]:
        login = c["login"]

        url_commits = f"https://api.github.com/repos/{repo}/commits"
        params = {"author": login, "since": since, "per_page": 1}
        r = requests.get(url_commits, headers=headers, params=params)

        if "Link" in r.headers:
            link = r.headers["Link"]
            last = link.split("page=")[1].split(">")[0]
            commits = int("".join(filter(str.isdigit, last)))
        else:
            commits = len(r.json()) if r.json() else 0

        if commits < min_commits:
            continue

        url_pr = "https://api.github.com/search/issues"
        params_pr = {"q": f"author:{login}+repo:{repo}+type:pr+created:>={since}"}
        pr_response = requests.get(url_pr, headers=headers, params=params_pr)
        pr_count = pr_response.json().get("total_count", 0)

        result.append({"login": login, "commits": commits, "prs": pr_count})

    result.sort(key=lambda x: x["commits"], reverse=True)
    return result[:5]


def plot_activity(contributors, repo):
    names = [c["login"] for c in contributors]
    commits = [c["commits"] for c in contributors]
    prs = [c["prs"] for c in contributors]

    x = range(len(names))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar([i - width / 2 for i in x], commits, width, label="Коммиты", color="skyblue")
    plt.bar([i + width / 2 for i in x], prs, width, label="Pull Requests", color="salmon")
    plt.xlabel("Контрибьюторы")
    plt.ylabel("Количество")
    plt.title(f"Топ активных контрибьюторов в {repo}")
    plt.xticks(x, names, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{repo.replace("/", "_")}_activity.png')
    plt.show()


repo = input("Введите репозиторий (owner/repo): ")
days = int(input("Выберите период (7/30/365 дней): "))
min_commits = int(input("Минимальное количество коммитов: "))

top = get_top_contributors(repo, days, min_commits)

print(f"\nТОП-5 активных контрибьюторов в '{repo}' за {days} дней:")
for i, c in enumerate(top, 1):
    print(f"{i}. @{c['login']} - {c['commits']} коммитов, {c['prs']} PR")

if top:
    plot_activity(top, repo)
