# csv cleaner

import csv
import pandas as pd


def find_duplicates(csv_file):
    df = pd.read_csv(csv_file)

    column_name = df.columns[1]

    # keep the first occurrence and mark the rest as duplicates
    duplicates = df[df.duplicated()]

    print("Duplicates:")
    count = 0
    for index, row in duplicates.iterrows():
        category = row["category"]
        title = row["title"]
        print(f"Category: {category:<10} Title: {title}")
        count += 1
    print(f"Total duplicates: {count}")


# Example usage
csv_file_path = "assets/csv/href.csv"
find_duplicates(csv_file_path)
