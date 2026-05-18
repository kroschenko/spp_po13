from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import requests

# Внешние зависимости: pip install requests matplotlib numpy


def get_trending_repos(language, date_from, min_stars):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"language:{language} created:>={date_from} stars:>={min_stars}",
        "sort": "stars",
        "order": "desc",
        "per_page": 10,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["items"]


def main():
    language = input("Введите язык программирования: ").strip()
    period = int(input("Выберите период (7 / 30 дней): ").strip())
    min_stars = input("Минимальное количество звёзд (по желанию): ").strip()
    min_stars = int(min_stars) if min_stars else 500

    date_from = (datetime.now() - timedelta(days=period)).strftime("%Y-%m-%d")
    print(
        f"\nАнализируем популярные репозитории на {language} за последние {period} дней..."
    )

    repos = get_trending_repos(language, date_from, min_stars)[:5]

    print("\nТОП-5 самых быстрорастущих проектов:")
    names, stars = [], []
    for i, repo in enumerate(repos, 1):
        desc = repo.get("description", "Нет описания") or "Нет описания"
        print(
            f"{i}. **{repo['full_name']}** (+{repo['stargazers_count']:,} ⭐) - {desc[:50]}"
        )
        names.append(repo["full_name"][:20])
        stars.append(repo["stargazers_count"])

    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(names)))
    graph_bars = plt.barh(names, stars, color=colors)
    plt.xlabel("Количество звёзд")
    plt.title(f"ТОП-5 популярных репозиториев на {language} за {period} дней")
    plt.gca().invert_yaxis()

    for graph_bar, star in zip(graph_bars, stars):
        plt.text(
            graph_bar.get_width() + max(stars) * 0.01,
            graph_bar.get_y() + graph_bar.get_height() / 2,
            f"{star:,}",
            va="center",
            fontsize=10,
        )

    plt.tight_layout()
    filename = f"trending_{language.lower()}.png"
    plt.savefig(filename, dpi=100)
    print(f"\nГрафики роста сохранены в '{filename}'")


if __name__ == "__main__":
    main()
