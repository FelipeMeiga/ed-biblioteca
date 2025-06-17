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

print(f"{len(books)} livros carregados")
print("Autores disponíveis:", [a for a in author_map.values() if a.get_availability()])
print("Editoras e quantos livros têm:", {p.name: len(p.books) for p in publisher_map.values()})
