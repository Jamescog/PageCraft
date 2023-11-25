from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import json
import os

CATEGORIES = [
    "philosophy",
    "business",
    "science",
    "christian",
    "religion",
    "psychology",
    "fiction",
    "programming",
    "crime",
    "self-help",
]

BASE_URL = "https://www.goodreads.com/shelf/show/"
COOKIES_FILE_PATH = "cookies.json"


def save_cookies(driver, path):
    with open(path, "w") as filehandler:
        json.dump(driver.get_cookies(), filehandler)


def load_cookies(driver, path):
    with open(path, "r") as cookiesfile:
        cookies = json.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_book_href():
    path = "assets/csv/href.csv"

    with open(path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["category", "title", "href"])

        driver = webdriver.Firefox()

        if os.path.exists(COOKIES_FILE_PATH):
            driver.get(
                "https://www.goodreads.com"
            )  # Need to load website before loading cookies
            load_cookies(driver, COOKIES_FILE_PATH)

        for category in CATEGORIES:
            for i in range(1, 11):
                url = f"{BASE_URL}{category}?page={i}"
                driver.get(url)

                # Save cookies after login
                if not os.path.exists(COOKIES_FILE_PATH):
                    input("Press enter to continue...")
                    save_cookies(driver, COOKIES_FILE_PATH)

                page = driver.page_source
                soup = BeautifulSoup(page, "html.parser")
                a_tags = soup.find_all("a", class_="leftAlignedImage")
                for tag in a_tags:
                    if len(tag.get("class")) == 1:
                        writer.writerow([category, tag.get("title"), tag.get("href")])

        driver.quit()


if __name__ == "__main__":
    get_book_href()
