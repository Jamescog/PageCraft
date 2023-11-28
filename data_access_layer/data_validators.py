from pydantic import BaseModel
from typing import Optional, List


class BookDetail(BaseModel):
    _id: Optional[str]
    title: str
    rating: float
    author: str
    genre: str
    description: str
    book_cover: str
    book_url: str


class Title(BaseModel):
    title: str
