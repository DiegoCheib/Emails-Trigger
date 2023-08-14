import tkinter as tk
from tkinter import ttk
import mysql.connector
from funcoes_clients import display_data_
import smtplib
from mailjet_rest import Client
from funcoes_clients import clients

marked_items = []
checked_items = []

font_client = ("Times", 12)


db = mysql.connector.connect(
    host="localhost",  # ou o endereço do servidor MySQL
    user="root",
    password="",
    database="emailstrigger",
)
mycursor = db.cursor()


def email(janela_main):
    global clients_table
    global texto_email
    global assunto_email_entry
    global janela_emails
    # Fechando a Janela Main
    janela_main.destroy()
    # Criar uma janela
    janela_emails = tk.Tk()
    # Tamanho Janela
    janela_emails.geometry("900x600")
    # Título Janela
    janela_emails.title("Email Script")

    # Exibindo as tabelas
    clients_table = ttk.Treeview(
        janela_emails,
        columns=("ID", "Clients Name", "Customer's email", "Select"),
        show="headings",
    )

    # Colocando Estilo no display
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("Treeview", rowheight=25, background="#CFD2CD")
    janela_emails.config(bg="#CFD2CD")

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

    # Coluna 4 da tabela, Checkbox
    clients_table.column("Select", width=200, minwidth=200, stretch=False)
    clients_table.heading("#4", text="Select")

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
    display_data_()

    # Ao clicarmos em qualquer area do display Altera o a 4 coluna, mostrando que foi selecionado
    clients_table.bind("<Button 1>", toggleCheck)

    # Lugar para escrita do assunto do Email
    assunto_email_label = tk.Label(janela_emails, text="Assunto:")
    assunto_email_label.place(x=100, y=330)
    assunto_email_label.config(background="#CFD2CD", font=font_client)
    assunto_email_entry = tk.Entry(janela_emails, width=40)
    assunto_email_entry.place(x=100, y=350)
    assunto_email_entry.config(fg="#252627", font=font_client)

    # Lugar para escrita do corpo do Email
    texto_email_label = tk.Label(janela_emails, text="Email:")
    texto_email_label.place(x=100, y=380)
    texto_email = tk.Text(janela_emails, width=60, height=10)
    texto_email.place(x=100, y=400)
    texto_email_label.config(background="#CFD2CD", font=font_client)
    texto_email.config(fg="#252627", font=font_client)
    # Butão e sua função
    email_enviar_button = tk.Button(
        janela_emails,
        width=5,
        text="Enviar",
        command=funcao_composta_email,
    )
    # Lugar do butão no plano Cartesiano
    email_enviar_button.place(x=600, y=540)
    email_enviar_button.config(background="#252627", fg="#fff", font="Times")

    back_button = tk.Button(janela_emails, text="Back", width=8, command=back_button_)
    back_button.place(x=755, y=540)
    back_button.config(background="#252627", fg="#fff", font="Times")

    # Mantendo janela clients aberta
    janela_emails.mainloop()


def back_button_():
    janela_emails.destroy()
    # Criando a janela principal
    janela_main = tk.Tk()
    # Tamanho Janela
    janela_main.geometry("900x600")
    # Título Janela
    janela_main.title("Email Trigger")

    fonte_main = ("Times", "16")
    # Butão para a área de clients
    clients_button = tk.Button(
        janela_main,
        text="Clients",
        height=5,
        width=25,
        command=lambda: clients(janela_main),
        font=fonte_main,
    )
    # Local do butão, plano cartesiano X e Y
    clients_button.place(x=120, y=205)
    # Butão para área de Script de Email
    email_button = tk.Button(
        janela_main,
        text="Emails",
        height=5,
        width=25,
        command=lambda: email(janela_main),
        font=fonte_main,
    )
    # Local do butão, plano cartesiano X e Y
    email_button.place(x=480, y=205)


def API_Mailjet():
    # Salvando os IDS marcados como CHECKED em uma variavel
    checked_items = get_checked_items()
    # LOG dos IDS salvos
    print(checked_items)
    # Salvado o conteúdo escrito no entry do assunto em uma variavel
    assunto_email_content = assunto_email_entry.get()
    # Salvando o Script/Corpo do email em uma variavel
    texto_email_content = texto_email.get("1.0", "end-1c")

    # Obtendo os itens marcados
    for item in checked_items:
        destinatario_email = item[
            "email"
        ]  # Salvando o email do destinatario previamente salvo em um dicionario em uma nova variavel escrita
        destinatario_email_name = item[
            "name"
        ]  # Salvando o nome do destinatario previamente salvo em um dicionario em uma nova variavel escrita
        mailjet = Client(
            auth=(
                "f5de26171d5bdc673e05a2ed5b0c2d30",  # API key
                "2f271cc7871cffb3d3e11aab0ec93ce4",  # My secret key
            ),
            version="v3.1",  # Versão do Mailjet sendo utilizada
        )

        data = {
            "Messages": [
                {
                    "From": {
                        "Email": "scriptemailportifolio@gmail.com",  # Email de sua empresa/ Remetente
                        "Name": "Teste Script",  # Seu nome
                    },
                    "To": [
                        {
                            "Email": f"{destinatario_email}",  # Email do destinatario
                            "Name": f"{destinatario_email_name}",  # Nome do destinatario
                        }
                    ],
                    # Assunto do Email a ser enviado
                    "Subject": assunto_email_content,
                    # Corpo do texto a ser enviado
                    "TextPart": texto_email_content,
                }
            ]
        }

        # Printa no console Sucess or Error( Se foi um sucesso o envio ou falha/erro)
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())


def funcao_composta_email():
    # Chama a função api_mailjet e após isso limpa seus campos e retorna ele em branco, para uma nova escrita
    API_Mailjet()
    limpar_campos()


def limpar_campos():
    # Após o envio do script os campos são voltados em branco
    assunto_email_entry.delete("0", "end")
    texto_email.delete("1.0", "end")


def get_checked_items():
    # Para cada item_id salvado previamente na lista marked_items( Cliente selecionados para envio), cria um dicionario com nome e email de cada cliente
    for item_id in marked_items:
        email, name = get_email_and_name_by_id(item_id)
        checked_items.append({"email": email, "name": name})
    # Retorna um dicionario salvo com os nomes, emails de cada cliente
    return checked_items


def get_email_and_name_by_id(item_id):
    # Salvando as informações do cliente pelo id na variavel values
    values = clients_table.item(item_id, "values")
    # Salva precisamente o email, nome do cliente, na lista(Values) anteriormente salvada
    email = values[2]
    name = values[1]
    # Retornando as variaveis
    return email, name


def toggleCheck(event):
    # Identificando e salvando numa variavel quando uma linha é clicada, assim alterando seu estado de unchecked para checked
    item_id = clients_table.identify_row(event.y)

    # Estado atual da linha ( Checked or Unchecked), o select está localizado na terceira coluna
    current_state = clients_table.item(item_id, "values")[3]

    # Se o estado for checked e  clicar novamente na linha será removido da lista e será mostrado e salvo como Unchecked
    if current_state == "checked":
        new_state = "unchecked"
        marked_items.remove(item_id)  # Remover item da lista

    # Se o estado for Unchecked e clicar novamente na linha será adicionado da lista e será mostrado e salvo como Checked
    else:
        new_state = "checked"
        marked_items.append(item_id)  # Adicionar item à lista

    clients_table.item(
        item_id, values=(clients_table.item(item_id, "values")[0:3] + (new_state,))
    )
    print(marked_items)


def display_data_():
    # Seleciona todos os itens de todas as colunas existentes no banco de dados
    mycursor.execute("SELECT * FROM clients")
    # Salva esses itens na variavel USERS
    users = mycursor.fetchall()
    # Para cada user existente na variavel users, salvada na linha de cima, Insere ele no TreeView, fazendo com que conseguimos exibir o banco de dados em tempo real
    for user in users:
        clients_table.insert("", "end", values=user + ("unchecked",))
