# book.py
from __future__ import annotations
from typing import Dict, List
from author import Author
from publisher import Publisher

class Book:
    def __init__(
        self,
        book_id: str,
        isbn: str,
        title: str,
        year: int,
        publisher: Publisher,
        authors: List[Author],
        total_copies: int,
        available_copies: int,
        average_rating: float
    ) -> None:
        self.id: str               = book_id
        self.isbn: str             = isbn
        self.title: str            = title
        self.year: int             = year
        self.publisher: Publisher  = publisher
        self.authors: List[Author] = authors
        self.total_copies: int     = total_copies
        self.available_copies: int = available_copies
        self.average_rating: float = average_rating

        self.publisher.add_book(self)
        for a in self.authors:
            a.add_book(self)

    def get_availability(self) -> bool:
        return self.available_copies > 0

    @staticmethod
    def search_book(books, title=None, isbn=None, author=None):
        results = books
        if title:
            results = [b for b in results if title.lower() in b.title.lower()]
        if isbn:
            results = [b for b in results if isbn == b.isbn]
        if author:
            results = [b for b in results if any(author.lower() in a.name.lower() for a in b.authors)]
        return results

    @classmethod
    def from_dict(cls, data: Dict, author_map: Dict[str, Author], publisher_map: Dict[str, Publisher] ) -> Book:
        pub_name = data['publisher']
        if pub_name not in publisher_map:
            publisher_map[pub_name] = Publisher.from_name(pub_name)
        pub = publisher_map[pub_name]

        authors: List[Author] = []
        for name in data.get('authors', []):
            if name not in author_map:
                author_map[name] = Author.from_name(name)
            authors.append(author_map[name])

        return cls(
            book_id=data['id'],
            isbn=data['isbn'],
            title=data['title'],
            year=data['year'],
            publisher=pub,
            authors=authors,
            total_copies=data['total_copies'],
            available_copies=data['available_copies'],
            average_rating=data.get('average_rating', 0.0)
        )

    def __repr__(self) -> str:
        return f"<Book {self.id}: {self.title}>"

   # return every information about the book
    def detalhes(self) -> str:
        autores = ", ".join([a.name for a in self.authors])
        return (
            f"Título: {self.title}\n"
            f"ISBN: {self.isbn}\n"
            f"Autores: {autores}\n"
            f"Ano: {self.year}\n"
            f"Editora: {self.publisher.name}\n"
            f"Total de cópias: {self.total_copies}\n"
            f"Cópias disponíveis: {self.available_copies}\n"
            f"Avaliação média: {self.average_rating}\n"
            "-----------------------------"
        )