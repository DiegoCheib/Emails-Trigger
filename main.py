import tkinter as tk
from tkinter import ttk
import mysql.connector
import smtplib
from mailjet_rest import Client

# ***********************************************************************************************************************#

db = mysql.connector.connect(
    host="localhost",  # ou o endereço do servidor MySQL
    user="root",
    password="",
    database="emailstrigger",
)
mycursor = db.cursor()


# ***********************************************************************************************************************#
def API_Mailjet():
    checked_items = get_checked_items()
    print(checked_items)

    texto_email_content = texto_email.get("1.0", "end-1c")
    assunto_email_content = assunto_email_entry.get()

    # Obtendo os itens marcados
    for item in checked_items:
        destinatario_email = item["email"]
        destinatario_email_name = item["name"]
        # Substitua 'YOUR_API_KEY' e 'YOUR_API_SECRET' pelas suas chaves da API
        mailjet = Client(
            auth=(
                "f5de26171d5bdc673e05a2ed5b0c2d30",
                "2f271cc7871cffb3d3e11aab0ec93ce4",
            ),
            version="v3.1",
        )

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": "scriptemailportifolio@gmail.com",
                        "Name": "Teste Script",
                    },
                    "To": [
                        {
                            "Email": f"{destinatario_email}",
                            "Name": f"{destinatario_email_name}",
                        }
                    ],
                    "Subject": assunto_email_content,
                    "TextPart": texto_email_content,
                }
            ]
        }

        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())


# ***********************************************************************************************************************#


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


# ***********************************************************************************************************************#
marked_items = []


def toggleCheck(event):
    item_id = clients_table.identify_row(event.y)
    current_state = clients_table.item(item_id, "values")[3]

    if current_state == "checked":
        new_state = "unchecked"
        marked_items.remove(item_id)  # Remover item da lista

    else:
        new_state = "checked"
        marked_items.append(item_id)  # Adicionar item à lista

    clients_table.item(
        item_id, values=(clients_table.item(item_id, "values")[0:3] + (new_state,))
    )
    print(marked_items)


# ***************************************************************************************************************************#


checked_items = []


def get_checked_items():
    global checked_items
    for item_id in marked_items:
        email, name = get_email_and_name_by_id(item_id)
        checked_items.append({"email": email, "name": name})

    return checked_items


# ***************************************************************************************************************************#


def limpar_campos():
    assunto_email_entry.delete("0", "end")
    texto_email.delete("1.0", "end")


# ***************************************************************************************************************************#
def funcao_composta_email():
    API_Mailjet()
    limpar_campos()


# ***************************************************************************************************************************#


def funcao_composta_add_client():
    add_data()
    limpar_campos()


# ***************************************************************************************************************************#


def funcao_composta_remove_client():
    remove_client()
    limpar_campos()


# ***************************************************************************************************************************#


def funcao_composta_update_client():
    update_data()
    limpar_campos()


# ***************************************************************************************************************************#


def get_email_and_name_by_id(item_id):
    values = clients_table.item(item_id, "values")
    email = values[2]  # Assuming email is the third column
    name = values[1]  # Assuming name is the second column
    return email, name


# ***************************************************************************************************************************#
def email():
    global texto_email
    global clients_table
    global assunto_email_entry

    # Fechando a Janela Main
    janela_main.destroy()
    # Criar uma janela
    janela_emails = tk.Tk()
    # Tamanho Janela
    janela_emails.geometry("900x600")
    # Título Janela
    janela_emails.title("Emails Windown")

    # Exibindo as tabelas
    clients_table = ttk.Treeview(
        janela_emails,
        columns=("ID", "Clients Name", "Customer's email", "Select"),
        show="headings",
    )
    clients_table.heading("#1", text="ID")
    clients_table.heading("#2", text="Clients Name")
    clients_table.heading("#3", text="Customer's email")
    clients_table.heading("#4", text="Select")
    # Colocando Estilo no display
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", rowheight=30)

    clients_table.tag_configure("checked", background="green")
    clients_table.tag_configure("unchecked", background="red")

    # Coluna 1 da tabela, ID
    clients_table.column("ID", width=50, minwidth=50, stretch=True)
    clients_table.heading("#1", text="ID")

    # Coluna 2 da tabela, Nome dos clients
    clients_table.column("Clients Name", width=200, minwidth=400, stretch=False)
    clients_table.heading("#2", text="Clients Name")

    # Coluna 3 da tabela, Email dos clients
    clients_table.column("Customer's email", width=400, minwidth=400, stretch=False)
    clients_table.heading("#3", text="Customer's email")

    # Coluna 4 da tabela, Checkbox
    clients_table.column("Select", width=200, minwidth=200, stretch=False)
    clients_table.heading("#4", text="")

    # X and Y da tabela
    clients_table.grid(row=0, column=0)
    scrollbar = ttk.Scrollbar(
        janela_emails, orient="vertical", command=clients_table.yview
    )
    # X and Y da Scrollbar
    scrollbar.place(relx=0.988, rely=0, relheight=1)

    # configuração da scrolbbar
    clients_table.configure(yscrollcommand=scrollbar.set)
    janela_emails.grid_rowconfigure(
        50,
        weight=30,
    )

    # Chamando Função para mostrar o banco de dados MySQl
    display_data()

    # Ao clicarmos em qualquer area do display Altera o a 4 coluna, mostrando que foi selecionado
    clients_table.bind("<Button 1>", toggleCheck)

    # Pega e salva os itens que foram selecionados

    assunto_email_label = tk.Label(janela_emails, text="Assunto:")
    assunto_email_label.place(x=100, y=340)
    assunto_email_entry = tk.Entry(janela_emails, width=40)
    assunto_email_entry.place(x=100, y=360)

    texto_email_label = tk.Label(janela_emails, text="Email:")
    texto_email_label.place(x=100, y=380)
    texto_email = tk.Text(janela_emails, width=60, height=10)
    texto_email.place(x=100, y=400)

    email_enviar_button = tk.Button(
        janela_emails, width=5, text="Enviar", command=funcao_composta_email
    )
    email_enviar_button.place(x=600, y=540)


# ***************************************************************************************************************************#


def display_data():
    global clients_table
    mycursor.execute("SELECT * FROM clients")
    users = mycursor.fetchall()

    for user in users:
        clients_table.insert("", "end", values=user + ("unchecked",))


# ***********************************************************************************************************************#


def sumir_widgets():
    global update_entry
    global update_label
    global update_button
    update_entry.destroy()
    update_label.destroy()
    update_button.destroy()


# ***********************************************************************************************************************#


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


# ***********************************************************************************************************************#


def update_data():
    global new_update_email_entry
    global new_update_name_entry
    global name_email
    global update_id
    update_name = new_update_name_entry.get()
    update_email = new_update_email_entry.get()
    update = f"UPDATE clients SET name = %s, email = %s WHERE ID = %s"
    values = (update_name, update_email, update_id)
    mycursor.execute(update, values)
    db.commit()


# ***********************************************************************************************************************#


def get_update_id():
    global update_id
    global new_update_button
    global new_update_email_entry
    global new_update_name_entry
    global name_email
    # Salvando o ID para atualizar os dados
    update_id = update_entry.get()
    # Selecionando o nome e email dos clients pelo ID escrito na linha de cima
    name_email = mycursor.execute(
        f"SELECT name,email FROM clients WHERE ID = {update_id}"
    )
    clients_database = mycursor.fetchall()
    sumir_widgets()
    # Ao clicar no butão update ira surgir estes espaços para poder atualizar as informações do cliente
    # Definindo o lugar para escrita do novo email e seu lugar na janela
    new_update_name_label = tk.Label(janela_clients, text="New client:")
    new_update_name_label.place(x=690, y=90)
    # Definindo o lugar para escrita do novo novo e seu lugar na janela
    new_update_name_entry = tk.Entry(janela_clients)
    new_update_name_entry.place(x=770, y=90)
    # Definindo a escrita do novo email na janela
    new_update_email_label = tk.Label(janela_clients, text="New Email:")
    new_update_email_label.place(x=690, y=120)
    # Definindo o lugar para escrita do novo email e seu lugar na janela
    new_update_email_entry = tk.Entry(janela_clients)
    new_update_email_entry.place(x=770, y=120)
    # Definindo o butão para atulizar os dados do cliente
    new_update_button = tk.Button(
        janela_clients, text="Update", width=10, command=update_data
    )
    new_update_button.place(x=760, y=150)


# ***********************************************************************************************************************#


def remove_client():
    global remove_entry
    # Pegando o id escrito
    id_remove = remove_entry.get()
    # Removendo o cliente pelo ID descrito anteriormente
    remove = f"DELETE FROM clients WHERE ID = {id_remove}"
    # Executando a remoção do cliente
    mycursor.execute(remove)
    # Salvando o banco de dados já sem o cliente removido
    db.commit()


# ***********************************************************************************************************************#


# Atualizar este butão
def update_display_data():
    clients_table.delete()
    display_data()


# ***************************************************************************************************************************#


def clients():
    global update_button
    global update_label
    global clients_table
    global update_entry
    global remove_entry
    global janela_clients
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
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", rowheight=60)

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

    # Chamando função para exibir o banco de dados
    display_data()
    # Lugar para a escrita do ID para saber em qual cliente atualizar os dados
    update_label = tk.Label(janela_clients, text="Id:", width=10)
    update_label.place(x=670, y=120)
    # Lugar para escrever o novo nome para dar update
    update_entry = tk.Entry(janela_clients)
    update_entry.place(x=720, y=120)

    # Butão para dar update no banco de dados
    update_button = tk.Button(
        janela_clients, text="Update", width=10, command=get_update_id
    )
    update_button.place(x=745, y=150)

    # Nome escrito antes do entry
    name_label = tk.Label(janela_clients, text="Nome:")
    name_label.place(x=690, y=240)
    # Espaço para escrita do nome
    name_entry = tk.Entry(janela_clients)
    name_entry.place(x=740, y=240)
    # Nome Escrito antes do entry
    email_label = tk.Label(janela_clients, text="Email:")
    email_label.place(x=690, y=270)
    # Espaço para escrita do email
    email_entry = tk.Entry(janela_clients)
    email_entry.place(x=740, y=270)
    Add_Clients = tk.Button(
        janela_clients,
        text="Add Client",
        width=10,
        command=lambda: add_data(name_entry, email_entry, success, success_str),
    )
    # Local do butão X e Y(Plano cartesiano)
    Add_Clients.place(x=745, y=300)
    # Escrita de sucesso ao adicionar um Nome e Email na tabela
    success = tk.StringVar()
    success_str = tk.Label(janela_clients, textvariable=success, width=10)
    success_str.place(x=705, y=200)

    # Lugar para a escrita do ID para saber em qual cliente atualizar os dados
    remove_label = tk.Label(janela_clients, text="Id:", width=10)
    remove_label.place(x=670, y=360)
    # Lugar para escrever o novo nome para dar update
    remove_entry = tk.Entry(janela_clients)
    remove_entry.place(x=720, y=360)
    # Definindo o butão para remover os dados do cliente
    remove_button = tk.Button(
        janela_clients, text="Remove", width=10, command=remove_client
    )
    remove_button.place(x=745, y=390)

    update_display_data_button = tk.Button(
        janela_clients, text="Atualizar", width=10, command=update_display_data
    )
    update_display_data_button.place(x=745, y=480)
    # Mantendo janela clients aberta
    janela_clients.mainloop()


# ***********************************************************************************************************************#

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
clients_button = tk.Button(
    janela_main, text="Emails", height=5, width=25, command=email
)
clients_button.place(x=350, y=100)

# button for Report
clients_button = tk.Button(janela_main, text="Report", height=5, width=25, command="")
clients_button.place(x=650, y=100)


# Mantendo ela aberta
janela_main.mainloop()
