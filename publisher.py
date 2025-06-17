from __future__ import annotations
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from book import Book  

class Publisher:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.books: List[Book] = []

    def add_book(self, book: Book) -> None:
        if book not in self.books:
            self.books.append(book)

    @classmethod
    def from_name(cls, name: str) -> Publisher:
        return cls(name)

    def __repr__(self) -> str:
        return f"<Publisher {self.name}>"