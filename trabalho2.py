import sqlite3
import tkinter as tk
from tkinter import ttk
from datetime import datetime


# ---------------------- BANCO DE DADOS ----------------------
def conectar():
    return sqlite3.connect("biblioteca2.db")


def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Livro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER,
        genero TEXT,
        quantidade INTEGER
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE,
        endereco TEXT,
        telefone TEXT,
        email TEXT UNIQUE
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Emprestimo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_livro INTEGER,
        data_emprestimo TEXT,
        data_prevista TEXT,
        data_devolucao TEXT,
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id),
        FOREIGN KEY (id_livro) REFERENCES Livro(id)
    )
    ''')

    con.commit()
    con.close()


# ---------------------- FUNÇÕES ----------------------

# ---- LIVROS ----
def adicionar_livro():
    janela = tk.Toplevel(root)
    janela.title("Adicionar Livro")
    janela.geometry("400x400")

    tk.Label(janela, text="Título").place(x=20, y=20)
    titulo = tk.Entry(janela)
    titulo.place(x=150, y=20)

    tk.Label(janela, text="Autor").place(x=20, y=60)
    autor = tk.Entry(janela)
    autor.place(x=150, y=60)

    tk.Label(janela, text="Ano de Publicação").place(x=20, y=100)
    ano = tk.Entry(janela)
    ano.place(x=150, y=100)

    tk.Label(janela, text="Gênero").place(x=20, y=140)
    genero = tk.Entry(janela)
    genero.place(x=150, y=140)

    tk.Label(janela, text="Quantidade").place(x=20, y=180)
    quantidade = tk.Entry(janela)
    quantidade.place(x=150, y=180)

    resultado = tk.Label(janela, text="")
    resultado.place(x=20, y=220)

    def salvar():
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute('''
                INSERT INTO Livro (titulo, autor, ano_publicacao, genero, quantidade)
                VALUES (?, ?, ?, ?, ?)
            ''', (titulo.get(), autor.get(), int(ano.get()), genero.get(), int(quantidade.get())))
            con.commit()
            con.close()
            resultado.config(text="Livro adicionado com sucesso!", fg="green")
        except Exception as e:
            resultado.config(text=f"Erro: {e}", fg="red")

    tk.Button(janela, bg="#5badf6", text="Salvar", command=salvar).place(x=150, y=260)


def listar_livros():
    janela = tk.Toplevel(root)
    janela.title("Lista de Livros")
    janela.geometry("700x400")

    tree = ttk.Treeview(janela, columns=("ID", "Título", "Autor", "Ano", "Gênero", "Qtd"), show="headings")
    
    # Cabeçalhos
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Autor", text="Autor")
    tree.heading("Ano", text="Ano")
    tree.heading("Gênero", text="Gênero")
    tree.heading("Qtd", text="Quantidade")
    
    # Larguras
    tree.column("ID", width=40)
    tree.column("Título", width=150)
    tree.column("Autor", width=120)
    tree.column("Ano", width=60)
    tree.column("Gênero", width=100)
    tree.column("Qtd", width=80)

    tree.place(x=10, y=10, width=680, height=350)

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM Livro")
    for row in cur.fetchall():
        tree.insert("", "end", values=row)
    con.close()



# ---- USUÁRIOS ----
def cadastrar_usuario():
    janela = tk.Toplevel(root)
    janela.title("Cadastrar Usuário")
    janela.geometry("400x400")

    tk.Label(janela, text="Nome").place(x=20, y=20)
    nome = tk.Entry(janela)
    nome.place(x=150, y=20)

    tk.Label(janela, text="CPF").place(x=20, y=60)
    cpf = tk.Entry(janela)
    cpf.place(x=150, y=60)

    tk.Label(janela, text="Endereço").place(x=20, y=100)
    endereco = tk.Entry(janela)
    endereco.place(x=150, y=100)

    tk.Label(janela, text="Telefone").place(x=20, y=140)
    telefone = tk.Entry(janela)
    telefone.place(x=150, y=140)

    tk.Label(janela, text="Email").place(x=20, y=180)
    email = tk.Entry(janela)
    email.place(x=150, y=180)

    resultado = tk.Label(janela, text="")
    resultado.place(x=20, y=220)

    def salvar():
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute('''
                INSERT INTO Usuario (nome, cpf, endereco, telefone, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome.get(), cpf.get(), endereco.get(), telefone.get(), email.get()))
            con.commit()
            con.close()
            resultado.config(text="Usuário cadastrado com sucesso!", fg="green")
        except Exception as e:
            resultado.config(text=f"Erro: {e}", fg="red")

    tk.Button(janela, bg="#5badf6", text="Salvar", command=salvar).place(x=150, y=260)


def listar_usuarios():
    janela = tk.Toplevel(root)
    janela.title("Lista de Usuários")
    janela.geometry("820x400")

    tree = ttk.Treeview(janela, columns=("ID", "Nome", "CPF", "Endereço", "Telefone", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("Endereço", text="Endereço")
    tree.heading("Telefone", text="Telefone")
    tree.heading("Email", text="Email")
    tree.place(x=10, y=10, width=800, height=350)

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM Usuario")
    for row in cur.fetchall():
        tree.insert("", "end", values=row)
    con.close()

# ---- EMPRÉSTIMO ----
def registrar_emprestimo():
    janela = tk.Toplevel(root)
    janela.title("Registrar Empréstimo")
    janela.geometry("400x300")

    tk.Label(janela, text="ID Usuário").place(x=20, y=20)
    id_usuario = tk.Entry(janela)
    id_usuario.place(x=150, y=20)

    tk.Label(janela, text="ID Livro").place(x=20, y=60)
    id_livro = tk.Entry(janela)
    id_livro.place(x=150, y=60)

    tk.Label(janela, text="Data Prevista (DD-MM-AAAA)").place(x=20, y=100)
    data_prevista = tk.Entry(janela)
    data_prevista.place(x=150, y=130)

    resultado = tk.Label(janela, text="")
    resultado.place(x=20, y=180)

    def salvar():
        try:
            data_emprestimo = datetime.now().strftime("%Y-%m-%d")
            data_prevista_formatada = datetime.strptime(data_prevista.get(), "%d-%m-%Y").strftime("%Y-%m-%d")

            con = conectar()
            cur = con.cursor()

            # VERIFICAR se o livro existe e se tem quantidade disponível
            cur.execute("SELECT quantidade FROM Livro WHERE id = ?", (id_livro.get(),))
            resultado_livro = cur.fetchone()

            if not resultado_livro:
                resultado.config(text="Livro não encontrado.", fg="red")
                return
            elif resultado_livro[0] <= 0:
                resultado.config(text="Livro indisponível.", fg="red")
                return

            # FAZER O EMPRÉSTIMO
            cur.execute('''
                INSERT INTO Emprestimo (id_usuario, id_livro, data_emprestimo, data_prevista, data_devolucao)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_usuario.get(), id_livro.get(), data_emprestimo, data_prevista_formatada, None))

            # ATUALIZAR A QUANTIDADE DE LIVROS
            cur.execute("UPDATE Livro SET quantidade = quantidade - 1 WHERE id = ?", (id_livro.get(),))

            con.commit()
            con.close()
            resultado.config(text="Empréstimo registrado!", fg="green")
        except Exception as e:
            resultado.config(text=f"Erro: {e}", fg="red")

    tk.Button(janela, bg="#5badf6", text="Salvar", command=salvar).place(x=150, y=220)


def listar_emprestimos():
    janela = tk.Toplevel(root)
    janela.title("Lista de Empréstimos")
    janela.geometry("1020x400")

    tree = ttk.Treeview(janela, columns=("ID", "Usuário", "Livro", "Emprestado", "Previsto", "Devolvido"), show="headings")
    tree.heading("ID", text="ID Empréstimo")
    tree.heading("Usuário", text="ID Usuário")
    tree.heading("Livro", text="ID Livro")
    tree.heading("Emprestado", text="Data Empréstimo")
    tree.heading("Previsto", text="Data Prevista")
    tree.heading("Devolvido", text="Data Devolução")

    # Define larguras para cada coluna para garantir visibilidade
    tree.column("ID", width=50)
    tree.column("Usuário", width=100)
    tree.column("Livro", width=100)
    tree.column("Emprestado", width=120)
    tree.column("Previsto", width=120)
    tree.column("Devolvido", width=120)

    tree.place(x=10, y=10, width=1000, height=350)

    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM Emprestimo")
    for row in cur.fetchall():
        tree.insert("", "end", values=row)
    con.close()



def devolver_livro():
    janela = tk.Toplevel(root)
    janela.title("Devolver Livro")
    janela.geometry("400x200")

    tk.Label(janela, text="ID do Empréstimo").place(x=20, y=20)
    id_emprestimo = tk.Entry(janela)
    id_emprestimo.place(x=150, y=20)

    resultado = tk.Label(janela, text="")
    resultado.place(x=20, y=100)

    def salvar():
        try:
            data_devolucao = datetime.now().strftime("%Y-%m-%d")

            con = conectar()
            cur = con.cursor()

            # 1. Verifica se o empréstimo existe
            cur.execute("SELECT id_livro, data_devolucao FROM Emprestimo WHERE id = ?", (id_emprestimo.get(),))
            dados = cur.fetchone()

            if not dados:
                resultado.config(text="Empréstimo não encontrado.", fg="red")
                return

            id_livro, devolvido = dados

            # 2. Verifica se já foi devolvido
            if devolvido:
                resultado.config(text="Este livro já foi devolvido.", fg="orange")
                return

            # 3. Atualiza a devolução e devolve o livro ao estoque
            cur.execute("UPDATE Emprestimo SET data_devolucao = ? WHERE id = ?", (data_devolucao, id_emprestimo.get()))
            cur.execute("UPDATE Livro SET quantidade = quantidade + 1 WHERE id = ?", (id_livro,))

            con.commit()
            con.close()
            resultado.config(text="Livro devolvido com sucesso!", fg="green")

        except Exception as e:
            resultado.config(text=f"Erro: {e}", fg="red")

    tk.Button(janela, text="Devolver", command=salvar).place(x=150, y=60)



# ---------------------- DROP DOWN ----------------------#

def executar_acao(opcao):
    if opcao == "Adicionar Livro":
        adicionar_livro()
    elif opcao == "Listar Livros":
        listar_livros()
    elif opcao == "Cadastrar Usuário":
        cadastrar_usuario()
    elif opcao == "Listar Usuários":
        listar_usuarios()
    elif opcao == "Registrar Empréstimo":
        registrar_emprestimo()
    elif opcao == "Listar Empréstimos":
        listar_emprestimos()
    elif opcao == "Devolver Livro":
        devolver_livro()

# ---------------------- INTERFACE ----------------------
criar_tabelas()

root = tk.Tk()
root.title("Sistema de Biblioteca")
root.geometry("500x400")

tk.Label(root, text="Menu da Biblioteca", bg="#9ef9df", font=("Arial", 20)).place(x=120, y=30)

opcoes = [
    "Adicionar Livro",
    "Listar Livros",
    "Cadastrar Usuário",
    "Listar Usuários",
    "Registrar Empréstimo",
    "Listar Empréstimos",
    "Devolver Livro"
]

selecionado = tk.StringVar()
selecionado.set("Opções")

combo = ttk.Combobox(root, values=opcoes, state="readonly", font=("Arial", 13))
combo.set("Opções")  # texto inicial exibido
combo.place(x=140, y=100)

# ---- BOTÃO EXECUTAR ----
tk.Button(root, text="Executar", width=20, height=2, bg="#5badf6", font=("Arial", 13),
          command=lambda: executar_acao(combo.get())).place(x=145, y=170)

# ---- BOTÃO SAIR ----
tk.Button(root, text="Sair", width=20, font=("Arial", 13), bg="#f96d66", command=root.quit).place(x=145, y=250)

root.configure(bg="#9ef9df")

root.mainloop()