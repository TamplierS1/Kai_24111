# садыков искандер 24111

import asyncio
import csv
import json

from bs4 import BeautifulSoup
import httpx

BASE_NEWS_URL = "https://almetyevsk.tatarstan.ru/novosti-7095949.htm"
BASE_REGIONS_URL = "https://msu.tatarstan.ru/mregions.htm"

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


async def fetch_page(client, page = 0, url = ''):
    if url == '':
        return None

    print(f"Запрос страницы {page}: {url}")

    try:
        response = await client.get(url, headers=HEADERS, timeout=15.0)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        items = soup.select("div.activity__item")
        if not items:
            print(f"  На странице {page} новостей не найдено.")
            return []

        page_titles = []
        for item in items:
            title = parse_news_item(item)
            if title:
                page_titles.append({"title": title})

        return page_titles
    except Exception as e:
        print(f"Ошибка при загрузке страницы {page}: {e}")
        return []


async def scrape_all_async():
    all_titles = []

    async with httpx.AsyncClient() as client:
        # tasks = [fetch_page(client, page) for page in range(1, max_pages + 1)]
        news_url = BASE_NEWS_URL
        regions_url = BASE_REGIONS_URL
        tasks = [fetch_page(client, 1, news_url), fetch_page(client, 0, regions_url)]

        results = await asyncio.gather(*tasks)

        for page_titles in results:
            all_titles.extend(page_titles)

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


async def main():
    news = await scrape_all_async(max_pages=1)
    print(f"Всего собрано: {len(news)}")
    save_csv(news)
    save_json(news)


if __name__ == "__main__":
    asyncio.run(main())
