import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
from time import time


def make_recommendation(title):
    with open("assets/pickle/vectorizer.pickle", "rb") as f:
        vectorizer = pickle.load(f)

    with open("assets/pickle/encodeded_matrix.pickle", "rb") as f:
        encodeded_matrix = pickle.load(f)

    input_vector = vectorizer.transform([title])
    cosine_similarities = linear_kernel(input_vector, encodeded_matrix)

    indices = np.argsort(cosine_similarities).flatten()[-11:][::-1]
    df = pd.read_csv("assets/csv/cleaned-data.csv")

    data = df["title"].iloc[indices].values.tolist()
    e_time = time()
    return data
