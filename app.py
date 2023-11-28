import uvicorn
from fastapi import FastAPI
from routes.get_book import router as get_books_router
from routes.get_recomendation import router as get_recomendation_router

title = """PageCraft"""
summary = (
    "Book information and Recommendation API -  Navigating Books, Crafting Suggestions"
)
description = """PageCraft
 is a book recommendation engine that uses Natural Language Processing to recommend books based on the user's input.

 The user can input a book title and the engine will return a list of 10 books that are similar to the input.
The engine uses a TF-IDF vectorizer to vectorize the book titles and a linear kernel to calculate the cosine similarity between the input and the corpus.

The corpus is a list of 5000 books that were scraped from Goodreads. The books were scraped using the Selenium  framework and the data was cleaned using Pandas. The data was then vectorized using Scikit-Learn's TF-IDF vectorizer and pickled for later use."""

version = "1.0.0"
contact = {
    "name": "Yaekob Demisse",
    # "url": "https://jamescog.com",
    "email": "jamescog72@gmail.com",
}
app = FastAPI(
    title=title,
    summary=summary,
    version=version,
    contact=contact,
    description=description,
)

app.include_router(get_books_router, tags=["Book Info"], prefix="/api/v1/books")
app.include_router(
    get_recomendation_router, tags=["Book Recommendation"], prefix="/api/v1/books"
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8900)
