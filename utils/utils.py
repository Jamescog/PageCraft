import pandas as pd
import nltk
import re
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download("stopwords")

df = pd.read_csv("assets/csv/book-details.csv")

stop_words = set(stopwords.words("english"))

total_rows = df.shape[0]


def print_percentage(current_row):
    percentage = (current_row / total_rows) * 100
    print(f"Cleaned: {percentage:.2f}%")


def clean_description(description):
    description = re.sub(r"[^a-zA-Z0-9]", " ", description)
    description = description.lower()
    description = nltk.word_tokenize(description)
    description = [word for word in description if word not in stop_words]
    description = [word for word in description if len(word) > 2]
    description = " ".join(description)
    return description


# Create a new column for cleaned descriptions
df["cleaned_description"] = ""

for index, row in df.iterrows():
    try:
        cleaned_desc = clean_description(row["description"])
        df.at[index, "cleaned_description"] = cleaned_desc
        print_percentage(index + 1)
    except Exception as e:
        print(f"Error: {e}")
        pass

# Save the cleaned data to a new CSV file
output_file = "assets/csv/cleaned-data.csv"
df.to_csv(output_file, index=False)

print(f"\nCleaned data saved to {output_file}")
