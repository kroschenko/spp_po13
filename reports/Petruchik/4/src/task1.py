import json
import requests


def fetch_top_repositories(keyword):
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc"
    params = {'per_page': 10}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('items', [])
    except requests.exceptions.RequestException as error:
        print(f"Ошибка при запросе: {error}")
        return []


def main():
    keyword = input("Введите ключевое слово для поиска репозиториев: ")
    print(f"Топ-10 репозиториев по запросу '{keyword}':")

    repos_data = []
    items = fetch_top_repositories(keyword)

    for i, repo in enumerate(items, 1):
        info = {
            "name": repo.get("full_name"),
            "description": repo.get("description"),
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "last_commit": repo.get("pushed_at")
        }
        repos_data.append(info)

        print(f"{i}. {info['name']} | ⭐ {info['stars']} | Forks: {info['forks']} "
              f"| Last commit: {info['last_commit']}")

    with open("github_top_repos.json", "w", encoding="utf-16") as file:
        json.dump(repos_data, file, indent=4, ensure_ascii=False)

    print("\nРезультаты сохранены в github_top_repos.json")


if __name__ == "__main__":
    main()
