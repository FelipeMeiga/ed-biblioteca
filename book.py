from __future__ import annotations
from typing import Dict, List
import json
from pathlib import Path
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
        average_rating: float,
        reservations: list[str] = None
    ) -> None:
        self.id: str = book_id
        self.isbn: str = isbn
        self.title: str = title
        self.year: int = year
        self.publisher: Publisher = publisher
        self.authors: List[Author] = authors
        self.total_copies: int = total_copies
        self.available_copies: int = available_copies
        self.average_rating: float = average_rating
        self.reservations: list[str] = reservations if reservations is not None else []

        self.publisher.add_book(self)
        for a in self.authors:
            a.add_book(self)

    def get_availability(self) -> bool:
        return self.available_copies > 0

    @staticmethod
    def search_book(
        books: list["Book"],
        query: str = "",
        field: str = "general"
    ) -> list["Book"]:
        q = query.strip().lower()
        if not q:
            return books

        if field == "title":
            return [b for b in books if q in b.title.lower()]

        if field == "isbn":
            return [b for b in books if q == b.isbn.lower()]

        if field == "author":
            return [
                b for b in books
                if any(q in a.name.lower() for a in b.authors)
            ]

        return [
            b for b in books
            if (
                q in b.title.lower()
                or q in b.isbn.lower()
                or any(q in a.name.lower() for a in b.authors)
                or q in b.publisher.name.lower()
                or (hasattr(b, "category") and q in b.category.lower())
            )
        ]

    @classmethod
    def from_dict(
        cls,
        data: Dict,
        author_map: Dict[str, Author],
        publisher_map: Dict[str, Publisher]
    ) -> "Book":
        pub_name = data['publisher']
        if pub_name not in publisher_map:
            publisher_map[pub_name] = Publisher.from_name(pub_name)
        pub = publisher_map[pub_name]

        authors: List[Author] = []
        for name in data.get('authors', []):
            if name not in author_map:
                author_map[name] = Author.from_name(name)
            authors.append(author_map[name])

        book = cls(
            book_id=data['id'],
            isbn=data['isbn'],
            title=data['title'],
            year=data['year'],
            publisher=pub,
            authors=authors,
            total_copies=data['total_copies'],
            available_copies=data['available_copies'],
            average_rating=data.get('average_rating', 0.0),
            reservations=data.get('reservations', [])
        )
        if 'category' in data:
            book.category = data['category']
        return book

    @classmethod
    def register_book(
        cls,
        data_path: Path,
        data: Dict,
        author_map: Dict[str, Author],
        publisher_map: Dict[str, Publisher]
    ) -> "Book":
        text = data_path.read_text(encoding="utf-8")
        db = json.loads(text) if text.strip() else {}

        books_list = db.get('books', [])
        if "reservations" not in data:
            data["reservations"] = []
        books_list.append(data)
        db['books'] = books_list

        data_path.write_text(
            json.dumps(db, ensure_ascii=False, indent=4),
            encoding="utf-8"
        )

        return cls.from_dict(data, author_map, publisher_map)

    def reserve(self, user: str, db_path: Path) -> bool:
        if self.available_copies > 0 and user not in self.reservations:
            self.reservations.append(user)
            self.available_copies -= 1
            self._update_json(db_path)
            return True
        return False

    def cancel_reservation(self, user: str, db_path: Path) -> bool:
        if user in self.reservations:
            self.reservations.remove(user)
            self.available_copies += 1
            self._update_json(db_path)
            return True
        return False

    def _update_json(self, db_path: Path) -> None:
        db = json.loads(db_path.read_text(encoding="utf-8"))
        for b in db.get("books", []):
            if b["id"] == self.id:
                b["available_copies"] = self.available_copies
                b["reservations"] = self.reservations
        db_path.write_text(json.dumps(db, ensure_ascii=False, indent=4), encoding="utf-8")

    def __repr__(self) -> str:
        return f"<Book {self.id}: {self.title}>"

    def detalhes(self) -> str:
        autores = ", ".join([a.name for a in self.authors])
        detalhes = (
            f"Título: {self.title}\n"
            f"ISBN: {self.isbn}\n"
            f"Autores: {autores}\n"
            f"Ano: {self.year}\n"
            f"Editora: {self.publisher.name}\n"
        )
        if hasattr(self, "category"):
            detalhes += f"Categoria: {self.category}\n"
        detalhes += (
            f"Total de cópias: {self.total_copies}\n"
            f"Cópias disponíveis: {self.available_copies}\n"
            f"Avaliação média: {self.average_rating}\n"
        )
        if self.reservations:
            detalhes += f"Reservas: {', '.join(self.reservations)}\n"
        detalhes += "-----------------------------"
        return detalhes