import tkinter as tk
from tkinter import ttk

global clients_table

clients_id = []

clients_name = [
    "test1",
    "test2",
    "test3",
    "test4",
    "test5",
    "test6",
    "test7",
    "test8",
    "Test9",
    "Test10",
]
clients_email = [
    "test1@gmail.com",
    "test2@gmail.com",
    "test3@gmail.com",
    "test4@gmail.com",
    "test5@gmail.com",
    "test6@gmail.com",
    "test7@gmail.com",
    "test8@gmail.com",
    "test9@gmail.com",
    "test10@gmail.com",
]


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

    # Chamando Função TableList
    TableList(clients_table)

    # Mantendo janela clients aberta
    janela_clients.mainloop()


# Adiciona todos os IDs, Nomes e Emails na table_clients
def TableList(self):
    contador = 0
    # Conseguindo os IDs dos clientes
    for client in range(0, len(clients_name)):
        clients_id.append([client + 1])
    # Inserindo Todos os IDs, Nomes e Emails
    for i in range(0, len(clients_name)):
        self.insert(
            "",
            "end",
            values=(
                clients_id[contador],
                clients_name[contador],
                clients_email[contador],
            ),
        )
        contador += 1
    return self


def add_data(name_get, email_get, success, success_str):
    new_name = name_get.get()  # Lê o Nome escrito
    clients_name.append(new_name)  # Adiciona o Nome escrito na lista clients_name
    new_email = email_get.get()  # Lê o email escrito
    clients_email.append(new_email)  # Adiciona o Email escrito na lista clients_email
    success.set("Sucess, Nome e email salvo!")
    success_str.after(3000, lambda: success.set(""))  # Remove a mensagem acima


# Criar uma janela
janela_main = tk.Tk()
# Tamanho Janela
janela_main.geometry("900x600")
# Título Janela
janela_main.title("Email Trigger")

# button for clients list
clients_button = tk.Button(
    janela_main, text="Clients", height=5, width=25, command=clients
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
print(clients_email, clients_name)
# Local do butão X e Y(Plano cartesiano)
Add_Clients.place(x=460, y=450)
# Escrita de sucesso ao adicionar um Nome e Email na tabela
success = tk.StringVar()
success_str = tk.Label(janela_main, textvariable=success, width=10)
success_str.place(x=705, y=200)

# Mantendo ela aberta
janela_main.mainloop()
