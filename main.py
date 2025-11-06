from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Modelo de dados
class Livro(BaseModel):
    titulo: str
    autor: str
    ano: str

# Conexão com PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="C0rr3t1vO",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Criar tabela
cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR(255),
        autor VARCHAR(255),
        ano VARCHAR(4)
    )
""")
conn.commit()

@app.post("/livros")
def cadastrar_livro(livro: Livro):
    cursor.execute("INSERT INTO livros (titulo, autor, ano) VALUES (%s, %s, %s)",
                   (livro.titulo, livro.autor, livro.ano))
    conn.commit()
    return {"mensagem": "Livro cadastrado com sucesso"}

@app.get("/livros")
def listar_livros():
    cursor.execute("SELECT titulo, autor, ano FROM livros")
    livros = cursor.fetchall()
    return [{"titulo": l[0], "autor": l[1], "ano": l[2]} for l in livros]

# Fechar conexão ao encerrar
cursor.close()
conn.close()