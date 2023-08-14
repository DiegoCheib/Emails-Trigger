import tkinter as tk
from tkinter import ttk
import mysql.connector


font_client = ("Times", 12)

db = mysql.connector.connect(
    host="localhost",  # Conexão do servidor MySQL
    user="root",
    password="",
    database="emailstrigger",
)
mycursor = db.cursor()


def clients(janela_main):
    global clients_table
    global janela_clients
    global name_entry
    global email_entry
    global update_button
    global update_label
    global update_entry
    global remove_entry

    # Fechando Janela Main
    janela_main.destroy()
    # Abrindo janela clients
    janela_clients = tk.Tk()
    # Tamanho Janela
    janela_clients.geometry("900x625")
    # Título da janela
    janela_clients.title("Clients")
    # Exibindo as tabelas
    clients_table = ttk.Treeview(
        janela_clients,
        selectmode="browse",
        columns=("ID", "Clients Name", "Customer's email"),
        show="headings",
    )
    # Style utilizado na exibição do banco de dados
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", rowheight=60, background="#CFD2CD")
    janela_clients.config(bg="#CFD2CD")

    # Aplicar o estilo personalizado à Treeview
    clients_table.config(style="Treeview")

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
    display_data_()
    # Lugar para a escrita do ID para saber em qual cliente atualizar os dados
    update_label = tk.Label(janela_clients, text="Id:", width=3)
    update_label.place(x=675, y=120)
    # Estilização update_label
    update_label.config(background="#CFD2CD", font=("Times", 12))

    # Lugar para escrever o novo nome para dar update
    update_entry = tk.Entry(janela_clients)
    update_entry.place(x=720, y=120)
    # Estilização update_entry
    update_entry.config(fg="#252627", font=font_client)
    # Butão para dar update no banco de dados
    update_button = tk.Button(
        janela_clients,
        text="Update",
        width=8,
        command=get_update_id,
    )
    # Local do butão plano cartesiano X e Y
    update_button.place(x=745, y=150)
    update_button.config(background="#252627", fg="#fff", font="Times")

    # Nome escrito antes do entry
    name_label = tk.Label(janela_clients, text="Nome:")
    name_label.place(x=690, y=240)
    # Estilização name_label
    name_label.config(background="#CFD2CD", font=font_client)

    # Espaço para escrita do nome
    name_entry = tk.Entry(janela_clients)
    name_entry.place(x=740, y=240)
    # Estilização name_entry
    name_entry.config(fg="#252627", font=font_client)

    # Nome Escrito antes do entry
    email_label = tk.Label(janela_clients, text="Email:")
    email_label.place(x=690, y=270)
    # Estilização email_label
    email_label.config(bg="#CFD2CD", font=font_client)
    # Espaço para escrita do email
    email_entry = tk.Entry(janela_clients)
    email_entry.place(x=740, y=270)
    # Estilização email_entry
    email_entry.config(background="#fff", fg="#252627", font=font_client)
    Add_Clients = tk.Button(
        janela_clients,
        text="Add Client",
        width=8,
        command=add_data,
    )
    # Local do butão X e Y(Plano cartesiano)
    Add_Clients.place(x=745, y=300)
    # Estilização Add_clients
    Add_Clients.config(background="#252627", fg="#fff", font="Times")
    # Lugar para a escrita do ID para saber em qual cliente atualizar os dados
    remove_label = tk.Label(janela_clients, text="Id:", width=4)
    remove_label.place(x=680, y=360)
    # Estilização remove_label
    remove_label.config(background="#CFD2CD", font=font_client)
    # Lugar para escrever o novo nome para dar update
    remove_entry = tk.Entry(janela_clients)
    remove_entry.place(x=720, y=360)
    remove_entry.config(background="#fff", fg="#252627", font=font_client)

    # Definindo o butão para remover os dados do cliente
    remove_button = tk.Button(
        janela_clients,
        text="Remove",
        width=8,
        command=remove_client,
    )
    # Local do butão no plano cartesiano X e Y
    remove_button.place(x=745, y=390)
    remove_button.config(background="#252627", fg="#fff", font="Times")

    # Definindo o butão para atualizar o banco de dados mostrado
    update_display_data_button = tk.Button(
        janela_clients, text="Atualizar", width=10, command=update_display_data
    )
    # Local do butão no plano cartesiano X e Y
    update_display_data_button.place(x=745, y=480)
    update_display_data_button.config(background="#252627", fg="#fff", font="Times")

    back_button = tk.Button(janela_clients, text="Back", width=8, command=back_button_)
    back_button.place(x=755, y=540)
    back_button.config(background="#252627", fg="#fff", font="Times")

    # Mantendo janela clients aberta
    janela_clients.mainloop()


def back_button_(janela_main):
    janela_clients.destroy()
    janela_main()


def display_data_():
    # Seleciona todos os itens de todas as colunas existentes no banco de dados
    mycursor.execute("SELECT * FROM clients")
    # Salva esses itens na variavel USERS
    users = mycursor.fetchall()
    # Para cada user existente na variavel users, salvada na linha de cima, Insere ele no TreeView, fazendo com que conseguimos exibir o banco de dados em tempo real
    for user in users:
        clients_table.insert("", "end", values=user + ("unchecked",))


def update_display_data():
    # Apaga o banco de dados anterior
    clients_table.delete(*clients_table.get_children())
    # Exibe ele novamente com as novas informações salvas
    display_data_()


def sumir_widgets():
    # Exclui as seguintes informações para a aparição de novas
    update_button.destroy()
    update_entry.destroy()
    update_label.destroy()


def add_data():
    new_name = name_entry.get()  # Lê o novo cliente
    new_email = email_entry.get()  # Lê o email do cliente escrito
    new_user_insert = (  # Inserindo novo usuario adicionado na tabela
        "INSERT INTO clients(name, email) VALUES(%s, %s)"
    )
    values = (new_name, new_email)
    # Executando a inserção no banco de dados
    mycursor.execute((new_user_insert), values)
    # Salvando o novo cliente no banco de dados
    db.commit()
    # Após clicar no butão e salvar as informações o Espaço para escrita é deixado em branco novamente
    name_entry.delete("0", "end")
    email_entry.delete("0", "end")


def update_data():
    # Salvando em uma variável os novos nomes para dar update no banco de dados
    update_name = new_update_name_entry.get()
    update_email = new_update_email_entry.get()
    # Comando para alterar o email, nome no banco de dados
    update = f"UPDATE clients SET name = %s, email = %s WHERE ID = %s"
    values = (update_name, update_email, update_id)
    # Executando o comando para alterar o email, nome no banco de dados
    mycursor.execute(update, values)
    # Após clicar no butão e salvar as informações o Espaço para escrita é deixado em branco novamente
    new_update_name_entry.delete("0", "end")
    new_update_email_entry.delete("0", "end")
    # Salvando as mudanças no banco de dados
    db.commit()


def get_update_id():
    global clients_database
    global name_email
    global update_id
    global new_update_email_entry
    global new_update_email_label
    global new_update_name_label
    global new_update_name_entry
    global new_update_button

    # Salvando o ID para atualizar os dados
    update_id = update_entry.get()
    # Selecionando o nome e email dos clients pelo ID escrito na linha de cima
    name_email = mycursor.execute(
        f"SELECT name,email FROM clients WHERE ID = {update_id}"
    )
    # Salva o nome, email selecionado na linha anterior em uma variável
    clients_database = mycursor.fetchall()

    # Chamando a função para fazer sumir o id_label, id_entry, id_button para poder aparecer os novos meios de escrita para adicionar o novo cliente no banco de dados
    sumir_widgets()

    # Definindo o lugar para escrita do novo email e seu lugar na janela
    new_update_name_label = tk.Label(janela_clients, text="New client:")
    new_update_name_label.place(x=690, y=90)
    new_update_name_label.config(background="#fff", fg="#252627", font=font_client)
    # Definindo o lugar para escrita do novo novo e seu lugar na janela
    new_update_name_entry = tk.Entry(janela_clients)
    new_update_name_entry.place(x=770, y=90)
    new_update_name_entry.config(background="#fff", fg="#252627", font=font_client)
    # Definindo a escrita do novo email na janela
    new_update_email_label = tk.Label(janela_clients, text="New Email:")
    new_update_email_label.place(x=690, y=120)
    new_update_email_label.config(background="#fff", fg="#252627", font=font_client)

    # Definindo o lugar para escrita do novo email e seu lugar na janela
    new_update_email_entry = tk.Entry(janela_clients)
    new_update_email_entry.place(x=770, y=120)
    new_update_email_entry.config(background="#fff", fg="#252627", font=font_client)
    # Definindo o butão para atulizar os dados do cliente
    new_update_button = tk.Button(
        janela_clients, text="Update", width=10, command=update_data
    )
    # Local do butão no plano cartesiano X e Y
    new_update_button.place(x=760, y=150)
    new_update_button.config(background="#252627", fg="#fff", font="Times")


def remove_client():
    # Salvando o id escrito em uma variavel
    id_remove = remove_entry.get()
    # Removendo o cliente pelo ID descrito anteriormente
    remove = f"DELETE FROM clients WHERE ID = {id_remove}"
    # Executando a remoção do cliente
    mycursor.execute(remove)
    # Após clicar no butão e salvar as informações o Espaço para escrita é deixado em branco novamente
    id_remove.delete("0", "end")
    # Salvando o banco de dados já sem o cliente removido
    db.commit()
