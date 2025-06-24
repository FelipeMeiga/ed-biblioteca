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

import json
from typing import Dict
from author import Author
from publisher import Publisher
from book import Book
import tkinter as tk
from tkinter import ttk, messagebox

with open('database.json', encoding='utf-8') as f:
    db = json.load(f)

author_map: Dict[str, Author] = {}
publisher_map: Dict[str, Publisher] = {}

books = []
for b in db['books']:
    books.append(Book.from_dict(b, author_map, publisher_map))

# ...existing code...

def buscar():
    criterio = criterio_var.get()
    valor = entrada.get()
    if criterio == "Título":
        resultados = Book.search_book(books, title=valor)
    elif criterio == "Autor":
        resultados = Book.search_book(books, author=valor)
    elif criterio == "ISBN":
        resultados = Book.search_book(books, isbn=valor)
    else:
        resultados = []
    texto_resultados.config(state=tk.NORMAL)
    texto_resultados.delete(1.0, tk.END)
    if resultados:
        for livro in resultados:
            texto_resultados.insert(tk.END, livro.detalhes() + "\n")
    else:
        texto_resultados.insert(tk.END, "Nenhum livro encontrado.\n")
    texto_resultados.config(state=tk.DISABLED)

def listar_todos():
    texto_resultados.config(state=tk.NORMAL)
    texto_resultados.delete(1.0, tk.END)
    for livro in books:
        texto_resultados.insert(tk.END, livro.detalhes() + "\n")
    texto_resultados.config(state=tk.DISABLED)

#GUI setup
root = tk.Tk()
root.title("Biblioteca")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

criterio_var = tk.StringVar(value="Título")
criterios = ["Título", "Autor", "ISBN"]
ttk.Label(frame, text="Buscar por:").grid(row=0, column=0, sticky="w")
criterio_menu = ttk.OptionMenu(frame, criterio_var, criterios[0], *criterios)
criterio_menu.grid(row=0, column=1, sticky="ew")

entrada = ttk.Entry(frame, width=30)
entrada.grid(row=0, column=2, padx=5)

buscar_btn = ttk.Button(frame, text="Buscar", command=buscar)
buscar_btn.grid(row=0, column=3, padx=5)

listar_btn = ttk.Button(frame, text="Listar todos", command=listar_todos)
listar_btn.grid(row=0, column=4, padx=5)

texto_resultados = tk.Text(frame, width=80, height=20, wrap=tk.WORD)
texto_resultados.grid(row=1, column=0, columnspan=5, pady=10)
texto_resultados.config(state=tk.DISABLED)

root.mainloop()