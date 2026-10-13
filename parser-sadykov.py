# садыков искандер 24111

import csv
import json
import time

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://almetyevsk.tatarstan.ru/novosti-7095949.htm"
DELAY = 1

PAGE_TEMPLATE = BASE_URL + "?page={page}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9",
}


def parse_news_item(item):
    link = item.select_one("a.activity__link")
    if link and link.get("title"):
        return link["title"].strip()
    span = item.select_one(".activity__text.vue-line-clamp")
    return span.get_text(strip=True) if span else None


def scrape_all(max_pages=5):
    all_titles = []
    for page in range(1, max_pages + 1):
        url = PAGE_TEMPLATE.format(page=page) if page > 1 else BASE_URL
        print(f"Страница {page}: {url}")

        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select("div.activity__item")
        if not items:
            print("  Новостей не найдено, останавливаемся.")
            break

        for item in items:
            title = parse_news_item(item)
            if title:
                all_titles.append({"title": title})

        if not soup.select_one("a.next, .pagination a.next, li.next a"):
            break

        time.sleep(DELAY)

    return all_titles


def save_csv(news, path="news.csv"):
    if not news:
        print("Нечего сохранять в CSV.")
        return
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title"])
        writer.writeheader()
        writer.writerows(news)
    print(f"CSV: {path} ({len(news)} записей)")


def save_json(news, path="news.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print(f"JSON: {path} ({len(news)} записей)")


def main():
    news = scrape_all(max_pages=5)
    print(f"Всего собрано: {len(news)}")
    save_csv(news)
    save_json(news)


if __name__ == "__main__":
    main()
