import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://localhost:5432"

def cadastrar_livro():
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    ano = entry_ano.get()

    if not titulo or not autor or not ano:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    response = requests.post(f"{API_URL}/livros", json={
        "titulo": titulo,
        "autor": autor,
        "ano": ano
    })

    if response.status_code == 200:
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        entry_titulo.delete(0, tk.END)
        entry_autor.delete(0, tk.END)
        entry_ano.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Não foi possível cadastrar o livro.")

def listar_livros():
    response = requests.get(f"{API_URL}/livros")
    if response.status_code == 200:
        livros = response.json()
        if not livros:
            messagebox.showinfo("Lista de livros", "Nenhum livro cadastrado.")
            return

        lista = ""
        for i, livro in enumerate(livros, start=1):
            lista += f"{i}. {livro['titulo']} - {livro['autor']} ({livro['ano']})\n"

        messagebox.showinfo("Livros cadastrados", lista)
    else:
        messagebox.showerror("Erro", "Não foi possível obter a lista de livros.")

#Tela Principal 
janela = tk.Tk()
janela.title("Cadastro de Livros")

#Entradas
tk.Label(janela, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_titulo = tk.Entry(janela, width=40)
entry_titulo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(janela, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_autor = tk.Entry(janela, width=40)
entry_autor.grid(row=1, column=1, padx=5, pady=5)

tk.Label(janela, text="Ano de lançamento:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_ano = tk.Entry(janela, width=40)
entry_ano.grid(row=2, column=1, padx=5, pady=5)

btn_cadastrar = tk.Button(janela, text="Cadastrar Livro", command=cadastrar_livro)
btn_cadastrar.grid(row=3, column=0, columnspan=2, pady=10)

btn_listar = tk.Button(janela, text="Listar Livros", command=listar_livros)
btn_listar.grid(row=4, column=0, columnspan=2, pady=5)

janela.mainloop()

