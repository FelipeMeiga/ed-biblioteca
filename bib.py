import json
from pathlib import Path

import streamlit as st

from author import Author
from publisher import Publisher
from book import Book

# --- Carrega dados ---
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database.json"
if not DB_PATH.exists():
    DB_PATH.write_text(json.dumps({"books": []}, ensure_ascii=False, indent=4), encoding="utf-8")

author_map: dict[str, Author] = {}
publisher_map: dict[str, Publisher] = {}
books: list[Book] = []

# Carrega instâncias
for entry in json.loads(DB_PATH.read_text(encoding="utf-8")).get("books", []):
    books.append(Book.from_dict(entry, author_map, publisher_map))

# --- UI Streamlit ---
st.set_page_config(page_title="Biblioteca", layout="wide")
st.title("📚 Biblioteca")

# Painel lateral
with st.sidebar:
    criterio = st.selectbox("Buscar por:", ["Geral", "Título", "Autor", "ISBN"], index=0)
    valor = st.text_input("Valor de busca")
    buscar = st.button("🔍 Buscar")
    listar_todos = st.button("📋 Listar todos")
    registrar = st.button("➕ Registrar livro")

if registrar:
    st.subheader("Registrar novo livro")
    with st.form("form_registrar"):
        new_id = st.text_input("ID")
        new_isbn = st.text_input("ISBN")
        new_title = st.text_input("Título")
        new_year = st.number_input("Ano", min_value=0, value=2025)
        new_publisher = st.text_input("Editora")
        new_authors = st.text_input("Autores (separados por vírgula)")
        new_total = st.number_input("Total de cópias", min_value=0, value=1)
        new_available = st.number_input("Cópias disponíveis", min_value=0, value=1)
        new_rating = st.number_input("Avaliação média", min_value=0.0, value=0.0, format="%.2f")
        new_category = st.text_input("Categoria (opcional)")
        submitted = st.form_submit_button("Registrar")
    if submitted:
        authors_list = [a.strip() for a in new_authors.split(",") if a.strip()]
        record = {
            "id": new_id,
            "isbn": new_isbn,
            "title": new_title,
            "year": int(new_year),
            "publisher": new_publisher,
            "authors": authors_list,
            "total_copies": int(new_total),
            "available_copies": int(new_available),
            "average_rating": float(new_rating)
        }
        if new_category:
            record["category"] = new_category
        try:
            new_book = Book.register_book(DB_PATH, record, author_map, publisher_map)
            books.append(new_book)
            st.success("Livro registrado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao registrar livro: {e}")

elif buscar:
    field_map = {"Geral": "general", "Título": "title", "Autor": "author", "ISBN": "isbn"}
    field = field_map.get(criterio, "general")
    resultados = Book.search_book(books, query=valor, field=field)
    st.subheader(f"Resultados para {criterio} = '{valor}':")
    if resultados:
        for livro in resultados:
            st.markdown(livro.detalhes().replace("\n", "  \n"))
    else:
        st.info("Nenhum livro encontrado.")

elif listar_todos:
    st.subheader("Todos os livros:")
    for livro in books:
        st.markdown(livro.detalhes().replace("\n", "  \n"))

else:
    st.write("Use a barra lateral para buscar, listar ou registrar livros.")