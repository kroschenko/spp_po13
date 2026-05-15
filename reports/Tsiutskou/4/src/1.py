import datetime
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt

TOKEN = "token"


def get_top_contributors(repo_name, days_count, min_commits_count):
    since = (datetime.now() - timedelta(days=days_count)).isoformat()

    headers = {"User-Agent": "Mozilla/5.0", "Authorization": f"token {TOKEN}"}

    url = f"https://api.github.com/repos/{repo_name}/contributors"
    response = requests.get(url, headers=headers, timeout=30)

    if response.status_code != 200:
        return []

    contributors = response.json()
    result = []

    for contributor in contributors[:20]:
        login = contributor["login"]

        url_commits = f"https://api.github.com/repos/{repo_name}/commits"
        params = {"author": login, "since": since, "per_page": 1}
        r = requests.get(url_commits, headers=headers, params=params, timeout=30)

        if "Link" in r.headers:
            link = r.headers["Link"]
            last = link.split("page=")[1].split(">")[0]
            commits = int("".join(filter(str.isdigit, last)))
        else:
            commits = len(r.json()) if r.json() else 0

        if commits < min_commits_count:
            continue

        url_pr = "https://api.github.com/search/issues"
        params_pr = {"q": f"author:{login}+repo:{repo_name}+type:pr+created:>={since}"}
        pr_response = requests.get(url_pr, headers=headers, params=params_pr, timeout=30)
        pr_count = pr_response.json().get("total_count", 0)

        result.append({"login": login, "commits": commits, "prs": pr_count})

    result.sort(key=lambda x: x["commits"], reverse=True)
    return result[:5]


def plot_activity(contributors, repo_name):
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
    plt.title(f"Топ активных контрибьюторов в {repo_name}")
    plt.xticks(x, names, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{repo_name.replace("/", "_")}_activity.png')
    plt.show()


if __name__ == "__main__":
    REPO = input("Введите репозиторий (owner/repo): ")
    DAYS = int(input("Выберите период (7/30/365 дней): "))
    MIN_COMMITS = int(input("Минимальное количество коммитов: "))

    TOP = get_top_contributors(REPO, DAYS, MIN_COMMITS)

    print(f"\nТОП-5 активных контрибьюторов в '{REPO}' за {DAYS} дней:")
    for i, c in enumerate(TOP, 1):
        print(f"{i}. @{c['login']} - {c['commits']} коммитов, {c['prs']} PR")

    if TOP:
        plot_activity(TOP, REPO)
