"""Модуль анализа популярных GitHub репозиториев по теме."""

import sys
from datetime import datetime, timezone
from collections import Counter

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ====== Константы ======
GITHUB_API_URL = "https://api.github.com/search/repositories"


def fetch_repositories(topic: str):
    """Запрос репозиториев с GitHub API."""
    params = {
        "q": topic,
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
    }

    response = requests.get(GITHUB_API_URL, params=params, timeout=10)

    if response.status_code != 200:
        print("Ошибка запроса к GitHub API")
        sys.exit(1)

    return response.json()["items"]


def build_dataframe(data):
    """Преобразование данных API в DataFrame."""
    repos = []

    for repo in data:
        repos.append({
            "name": repo["full_name"],
            "language": repo["language"] or "Unknown",
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "issues": repo["open_issues_count"],
            "updated_at": repo["updated_at"],
        })

    return pd.DataFrame(repos)


def analyze_languages(df):
    """Анализ популярных языков."""
    language_counts = Counter(df["language"])
    total = sum(language_counts.values())

    language_percent = {
        lang: round(count / total * 100, 2)
        for lang, count in language_counts.items()
    }

    return sorted(language_percent.items(), key=lambda x: x[1], reverse=True)


def analyze_repositories(df):
    """Анализ репозиториев."""
    top_repo = df.loc[df["stars"].idxmax()]
    avg_forks = df["forks"].mean()

    return top_repo, avg_forks


def analyze_activity(df):
    """Анализ активности обновлений."""
    df["updated_at"] = pd.to_datetime(df["updated_at"])
    now = datetime.now(timezone.utc)

    df["days_since_update"] = (now - df["updated_at"]).dt.days

    old_repos = df[df["days_since_update"] > 365]
    percent_old = len(old_repos) / len(df) * 100

    return df, percent_old


def plot_languages(sorted_languages, topic: str):
    """График популярных языков."""
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 6))
    top_langs = dict(sorted_languages[:10])

    sns.barplot(
        x=list(top_langs.values()),
        y=list(top_langs.keys())
    )

    plt.title(f"Популярные языки ({topic})")
    plt.xlabel("Процент")
    plt.ylabel("Язык")
    plt.tight_layout()
    plt.savefig("languages.png")


def plot_popularity(df):
    """График популярности."""
    plt.figure(figsize=(8, 6))
    plt.scatter(df["stars"], df["forks"])

    plt.title("Популярность репозиториев")
    plt.xlabel("Звезды")
    plt.ylabel("Форки")
    plt.tight_layout()
    plt.savefig("popularity.png")


def plot_aging(df):
    """График устаревания репозиториев."""
    plt.figure(figsize=(8, 6))
    sns.histplot(df["days_since_update"], bins=20)

    plt.title("Возраст последнего обновления (в днях)")
    plt.xlabel("Дни")
    plt.ylabel("Количество репозиториев")
    plt.tight_layout()
    plt.savefig("aging.png")


def main():
    """Точка входа."""
    topic = input("Введите тему для анализа: ")

    print(f'Анализируем 100 популярных репозиториев по теме "{topic}"...')

    data = fetch_repositories(topic)
    df = build_dataframe(data)

    sorted_languages = analyze_languages(df)
    top_repo, avg_forks = analyze_repositories(df)
    df, percent_old = analyze_activity(df)

    print("\nСамые популярные языки:")
    for lang, percent in sorted_languages[:5]:
        print(f"- {lang} ({percent}%)")

    print(f'\nСамый звёздный репозиторий: "{top_repo["name"]}" ({top_repo["stars"]} звёзд)')
    print(f"Среднее количество форков: {round(avg_forks, 1)}")
    print(f"{round(percent_old)}% репозиториев не обновлялись больше года!")

    plot_languages(sorted_languages, topic)
    plot_popularity(df)
    plot_aging(df)

    print("\nГрафики сохранены: languages.png, popularity.png, aging.png")


if __name__ == "__main__":
    main()
