from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle

vectorizer = TfidfVectorizer()

df = pd.read_csv("assets/csv/cleaned-data.csv")

df.dropna(inplace=True)
df["combined"] = (
    df["top_genra"].apply(lambda x: x.replace("|", " ")) + df["cleaned_description"]
)


model_matrix = vectorizer.fit(df["combined"])
encodeded_matrix = vectorizer.transform(df["combined"])
# the second one is the encodeded matrix
with open("assets/pickle/vectorizer.pickle", "wb") as f:
    pickle.dump(model_matrix, f)

with open("assets/pickle/encodeded_matrix.pickle", "wb") as f:
    pickle.dump(encodeded_matrix, f)
