from bs4 import BeautifulSoup
import os


def get_file_data(file_path):
    data = []
    with open(file_path, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        a_tag = soup.find_all("a", class_="leftAlignedImage")
        for tag in a_tag:
            if len(tag.get("class")) == 1:
                data.append((tag.get("title"), tag.get("href")))

        return data[::-1]
