# author.py
from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from book import Book

class Author:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        if book not in self.books:
            self.books.append(book)

    def get_availability(self) -> bool:
        return any(book.available_copies > 0 for book in self.books)

    @classmethod
    def from_name(cls, name: str) -> Author:
        return cls(name)

    def __repr__(self) -> str:
        return f"<Author {self.name}>"
