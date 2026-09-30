import asyncio
import csv
import json
from pathlib import Path
from pprint import pprint

import httpx
import trafilatura
import trafilatura.settings
from bs4 import BeautifulSoup


async def fetch_articles(client, url) -> str:
    try:
        response = await client.get(url)
        return response.text
    except Exception as e:
        error_str = f"Error scraping {url}: {e}"
        print(error_str)
        return error_str


async def extract_content(html) -> trafilatura.settings.Document | None:
    content = await asyncio.to_thread(
        trafilatura.extract_with_metadata, html, output_format="markdown"
    )
    return content


def write_article_text_to_disk(filename, text) -> None:
    with open(filename, "x", newline="", encoding="utf-8-sig") as f:
        f.write(text)


async def main() -> None:
    # Собираем ссылки на статьи с HackerNews
    response = await httpx.AsyncClient().get("https://news.ycombinator.com/")
    soup = BeautifulSoup(response.text, "html.parser")

    spans = soup.find_all("span", class_="titleline")
    links = []
    titles = []
    for span in spans:
        link = span.a
        if (
            link is None
            or not str(link["href"]).startswith("https")
            or link.string is None
        ):
            continue

        links.append(str(link["href"]))
        titles.append(link.string)

    pprint(links, indent=4)

    async with httpx.AsyncClient() as client:
        # Скачиваем html статьи со всех собранных ссылок
        tasks = [fetch_articles(client, url) for url in links]
        articles_html = await asyncio.gather(*tasks)

        # Извлекаем контент из скачанных статей
        tasks = [extract_content(html) for html in articles_html]
        articles = await asyncio.gather(*tasks)

        # Конвертируем статьи из str в словарь с метаданными
        articles_with_metadata = []
        for article, link, title in zip(articles, links, titles):
            try:
                if article is None:
                    continue

                articles_with_metadata.append(
                    {
                        "Заголовок": title,
                        "Ссылка": link,
                        "Автор": article.author,
                        "Дата": article.date,
                    }
                )
            except json.JSONDecodeError as e:
                articles_with_metadata.append(
                    {
                        "Заголовок": "Ошибка JSON парсинга",
                        "Ссылка": e.msg,
                        "Автор": "",
                        "Дата": "",
                    }
                )

        # Записываем метаданные в CSV файл
        with open(
            "news_metadata.csv", "w", newline="", encoding="utf-8-sig"
        ) as csvfile:
            fieldnames = ["Заголовок", "Ссылка", "Автор", "Дата"]
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(articles_with_metadata)

        # Записываем текст статей в отдельные Markdown файлы
        Path("articles").mkdir(exist_ok=True)
        for article, title in zip(articles, titles):
            if article is None:
                continue

            title = (
                "articles/"
                + "".join(char for char in title if char.isalnum() or char.isspace())
                + ".md"
            )
            await asyncio.to_thread(
                write_article_text_to_disk,
                title,
                article.text,
            )


asyncio.run(main())
