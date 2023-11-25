from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import csv
from datetime import datetime, timedelta
from time import sleep

BASE_URL = "https://www.goodreads.com"


def send_notification(message):
    bot_token = "5640774466:AAH4fC0WZIq0SMnqkM6Our0NrQbg1EHJDc8"
    user_id = 144376682

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": user_id, "text": message}

    requests.post(url, data=data)
    return True


def load_cookies(driver, path):
    """
    Load cookies into the WebDriver.

    Parameters:
    - driver: WebDriver instance
    - path: Path to the cookies file
    """
    with open(path, "r") as cookiesfile:
        cookies = json.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_book_details():
    """
    Scrape book details from Goodreads and save them to a CSV file.
    """
    path_to_read = "assets/csv/href.csv"
    path_to_write = "assets/csv/book-details.csv"
    df = pd.read_csv(path_to_read)

    with open(path_to_write, "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "category",
                "title",
                "author",
                "rating",
                "description",
                "top_genra",
                "book_covor",
                "book_url",
            ]
        )
        curr_time = datetime.now()
        for i, row in df.iterrows():
            url = BASE_URL + row["href"]
            try:
                page = requests.get(url)
                soup = BeautifulSoup(page.text, "html.parser")
                title = soup.find("h1", class_=["Text", "Text__title1"]).text.strip()
                author = soup.find("span", class_="ContributorLink__name").text.strip()
                rating = soup.find(
                    "div", class_="RatingStatistics__rating"
                ).text.strip()
                top_genera = [
                    genra.find("span").text.strip()
                    for genra in soup.find_all(
                        "span", class_="BookPageMetadataSection__genreButton"
                    )
                ]
                description = soup.find("span", class_="Formatted").text.strip()
                book_covor = soup.find("img", class_="ResponsiveImage").get("src")
                writer.writerow(
                    [
                        row["category"],
                        title,
                        author,
                        rating,
                        description,
                        "|".join(top_genera),
                        book_covor,
                        url,
                    ]
                )
                sleep(0.5)
                if datetime.now() > curr_time + timedelta(minutes=5):
                    send_notification(
                        f"Scraped {i + 1} rows out of {len(df)} rows. {round((i + 1) / len(df) * 100, 2)}% done."
                    )
                    curr_time = datetime.now()
            except Exception as e:
                print(
                    f"An exception occurred for row {i + 1}: {str(e)}. Skipping to the next row."
                )
                send_notification(
                    f"An exception occurred for row {i + 1}:  Book Name: {row['title']} error: {str(e)}."
                )
                continue


if __name__ == "__main__":
    get_book_details()
