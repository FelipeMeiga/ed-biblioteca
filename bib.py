import json
from typing import Dict
from author import Author
from publisher import Publisher
from book import Book

with open('database.json', encoding='utf-8') as f:
    db = json.load(f)

author_map: Dict[str, Author] = {}
publisher_map: Dict[str, Publisher] = {}

books = []
for b in db['books']:
    books.append(Book.from_dict(b, author_map, publisher_map))

print(f"{len(books)} books carregados")
print("Autores disponíveis:", [a for a in author_map.values() if a.get_availability()])
print("Editoras e quantos books têm:", {p.name: len(p.books) for p in publisher_map.values()})

#buscar título
results = Book.search_book(books, title="1984")
for book in results:
    print(book)

#buscar autor
results = Book.search_book(books, author="George Orwell")
for book in results:
    print(book)

#buscar ISBN
results = Book.search_book(books, isbn="9788501322994")
for book in results:
    print(book)