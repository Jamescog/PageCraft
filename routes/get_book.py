"""FastAPI Book API

This module provides a set of API endpoints for managing and interacting with a book database.
"""

from fastapi import APIRouter, HTTPException
from data_access_layer.db import DataBaseManager
from data_access_layer.data_validators import BookDetail, Title

router = APIRouter()

# Initialize the database manager
router.db = DataBaseManager()


@router.get(
    "/get_by_title/{title}",
    summary="Fetch a Book by Title",
    description="This endpoint fetches a book from the database using its title. The title must be an exact match.",
)
async def get_by_title(title: str) -> BookDetail:
    """Fetch a book by its title.

    Args:
        title (str): The title of the book.

    Returns:
        dict: Information about the book.

    Raises:
        HTTPException: If the book is not found, raises a 404 status code.
    """
    book = router.db.get_one_by_title(title)

    if book:
        book["_id"] = str(book["_id"])
        return book

    raise HTTPException(status_code=404, detail="Book not found")


@router.get(
    "/get_random",
    summary="Fetch a Random Book",
    description="This endpoint fetches a random book from the database. The result varies each time the endpoint is called.",
)
async def get_random():
    """Fetch a random book.

    Returns:
        dict: Information about the random book.
    """
    book = router.db.get_random()
    book["_id"] = str(book["_id"])
    return book


@router.get(
    "/search",
    summary="Search Books by Title",
    description="This endpoint searches for books in the database using a search term.",
)
async def search(search_term: str, rating: float = 0.0, limit: int = 10, skip: int = 0):
    """Search for books by title.

    Args:
        search_term (str): The search term.

    Returns:
        List[dict]: A list of books that match the search term.
    """
    books = router.db.search(search_term, rating, limit)

    for book in books:
        book["_id"] = str(book["_id"])
    return books


@router.get(
    "/search_by_author",
    summary="Search Books by Author",
    description="This endpoint searches for books in the database using an author's name.",
)
async def search_by_author(author_name: str):
    """Search for books by author.

    Args:
        author_name (str): The author's name.

    Returns:
        List[dict]: A list of books that match the author's name.
    """
    books = router.db.search_by_author(author_name)

    for book in books:
        book["_id"] = str(book["_id"])
    return books
