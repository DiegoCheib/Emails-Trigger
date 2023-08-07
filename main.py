import tkinter as tk
from tkinter import ttk
import mysql.connector

global clients_table

db = mysql.connector.connect(
    host="localhost",  # ou o endereço do servidor MySQL
    user="root",
    password="",
    database="emailstrigger",
)
mycursor = db.cursor()


def database():
    db = mysql.connector.connect(
        host="localhost",  # ou o endereço do servidor MySQL
        user="root",
        password="",
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS emailstrigger ")
    # Criar a tabela se não existir
    mycursor.execute(
        """
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(40),
        email VARCHAR(150) UNIQUE
    )
    """
    )
    # Commit as mudanças e fechar a conexão
    db.commit()


def display_data():
    global clients_table
    mycursor.execute("SELECT * FROM clients")
    users = mycursor.fetchall()

    for user in users:
        clients_table.insert("", "end", values=user)


def add_data(name_get, email_get, success, success_str):
    new_name = name_get.get()  # Lê o Nome escrito
    new_email = email_get.get()  # Lê o email escrito
    new_user_insert = (  # Inserindo novo usuario adicionado na tabela
        "INSERT INTO clients(name, email) VALUES(%s, %s)"
    )
    values = (new_name, new_email)
    mycursor.execute((new_user_insert), values)
    success.set("Sucess, Nome e email salvo!")
    db.commit()
    success_str.after(3000, lambda: success.set(""))  # Remove a mensagem acima


def clients():
    global clients_table
    # Fechando Janela Main
    janela_main.destroy()
    # Abrindo janela clients
    janela_clients = tk.Tk()
    # Tamanho Janela
    janela_clients.geometry("900x600")
    # Exibindo as tabelas
    clients_table = ttk.Treeview(
        janela_clients,
        selectmode="browse",
        columns=("ID", "Clients Name", "Customer's email"),
        show="headings",
    )
    s=ttk.Style()
    s.theme_use('clam')
    s.configure('Treeview', rowheight=60)


    # Coluna 1 da tabela, ID
    clients_table.column("ID", width=50, minwidth=50, stretch=True)
    clients_table.heading("#1", text="ID")

    # Coluna 2 da tabela, Nome dos clients
    clients_table.column("Clients Name", width=200, minwidth=400, stretch=False)
    clients_table.heading("#2", text="Clients Name")

    # Coluna 3 da tabela, Email dos clients
    clients_table.column("Customer's email", width=400, minwidth=400, stretch=False)
    clients_table.heading("#3", text="Customer's email")

    # X and Y da tabela
    clients_table.grid(row=0, column=0)
    scrollbar = ttk.Scrollbar(
        janela_clients, orient="vertical", command=clients_table.yview
    )
    # X and Y da Scrollbar
    scrollbar.place(x=650, relheight=1)
    # configuração da scrolbbar
    clients_table.configure(yscrollcommand=scrollbar.set)
    janela_clients.grid_rowconfigure(
        100,
        weight=1,
    )

    # Diminua o tamanho da barra de rolagem

    # Chamando função para exibir o banco de dados
    display_data()

    # Butão para dar update no banco de dados
    update_button = tk.Button(
        janela_clients,
        text="Update",
        width=10,
    )
    update_button.place(x=745, y=150)
    # Mantendo janela clients aberta
    janela_clients.mainloop()


# Criar uma janela
janela_main = tk.Tk()
# Tamanho Janela
janela_main.geometry("900x600")
# Título Janela
janela_main.title("Email Trigger")

# button for clients list
clients_button = tk.Button(
    janela_main, text="Clients", height=5, width=25, command=(clients)
)
clients_button.place(x=50, y=100)

# button for email script
clients_button = tk.Button(janela_main, text="Emails", height=5, width=25, command="")
clients_button.place(x=350, y=100)

# button for Report
clients_button = tk.Button(janela_main, text="Report", height=5, width=25, command="")
clients_button.place(x=650, y=100)


# Nome escrito antes do entry
name_label = tk.Label(janela_main, text="Nome:")
name_label.place(x=400, y=350)
# Espaço para escrita do nome
name_entry = tk.Entry(janela_main)
name_entry.place(x=450, y=350)
# Nome Escrito antes do entry
email_label = tk.Label(janela_main, text="Email:")
email_label.place(x=400, y=400)
# Espaço para escrita do email
email_entry = tk.Entry(janela_main)
email_entry.place(x=450, y=400)
Add_Clients = tk.Button(
    janela_main,
    text="Add Client",
    width=10,
    command=lambda: add_data(name_entry, email_entry, success, success_str),
)
# Local do butão X e Y(Plano cartesiano)
Add_Clients.place(x=460, y=450)
# Escrita de sucesso ao adicionar um Nome e Email na tabela
success = tk.StringVar()
success_str = tk.Label(janela_main, textvariable=success, width=10)
success_str.place(x=705, y=200)

# Mantendo ela aberta
janela_main.mainloop()
