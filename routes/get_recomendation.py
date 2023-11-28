"""FastAPI Book Recommendation API

This module provides a set of API endpoints for generating book recommendations using a recommendation engine.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from data_access_layer.db import DataBaseManager
from engine.recommender import make_recommendation

router = APIRouter()

# Initialize the database manager
router.db = DataBaseManager()


@router.get(
    "/get_recommendation/{title}",
    summary="Fetch Book Recommendations",
    description="This endpoint fetches book recommendations based on the provided title.",
)
async def get_recommendation(title: str) -> List[str]:
    """Fetch book recommendations by title.

    Args:
        title (str): The title of the book.

    Returns:
        List[str]: List of recommended book titles.

    Raises:
        HTTPException: If no recommendations are found, raises a 404 status code.
    """
    books = make_recommendation(title)
    if books:
        return books

    raise HTTPException(status_code=404, detail="Book not found")


@router.get(
    "/recommend-random",
    summary="Fetch Random Book Recommendation",
    description="This endpoint fetches a random book recommendation with a randomly selected title.",
)
async def get_random_recommendation() -> dict:
    """Fetch a random book recommendation.

    Returns:
        dict: Information about the recommended book and its recommendations.
    """
    title = router.db.get_random()["title"]
    books = make_recommendation(title)
    if books:
        data = {"title": title, "recommendation": books}
        return data

    raise HTTPException(status_code=404, detail="Book not found")


@router.get(
    "/recommend-with-data/{title}",
    summary="Fetch Book Recommendation with Additional Data",
    description="This endpoint fetches book recommendations with additional data based on the provided title.",
)
async def get_recommendation_with_data(title: str) -> dict:
    """Fetch book recommendations with additional data by title.

    Args:
        title (str): The title of the book.

    Returns:
        dict: Information about the recommended books, the given book, and their details.

    Raises:
        HTTPException: If no recommendations are found, raises a 404 status code.
    """
    books = make_recommendation(title)
    if books:
        recommendation_data = router.db.get_many_by__in(books)
        [book.update({"_id": str(book["_id"])}) for book in recommendation_data]

        the_book = router.db.get_one_by_title(title)
        the_book["_id"] = str(the_book["_id"])

        data = {
            "title": title,
            "recommendation": recommendation_data,
            "the_book": the_book,
        }
        return data

    raise HTTPException(status_code=404, detail="Book not found")


@router.get(
    "/todays",
    summary="Today's Book Selection",
    description="This endpoint fetches the book selection of the day. The selection changes every 24 hours.",
)
async def todays_selection():
    """Fetch today's book selection.

    Returns:
        dict: Information about the selected book.
    """
    book = router.db.get_todays_selection()
    book["_id"] = str(book["_id"])
    return book
