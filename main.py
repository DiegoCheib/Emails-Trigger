import tkinter as tk
from tkinter import ttk
import mysql.connector
import smtplib
from mailjet_rest import Client
from funcoes_clients import *
from funcoes_email import *

# ***********************************************************************************************************************#

db = mysql.connector.connect(
    host="localhost",  # ou o endereço do servidor MySQL
    user="root",
    password="",
    database="emailstrigger",
)
mycursor = db.cursor()


# ***********************************************************************************************************************#
def database():
    db = mysql.connector.connect(
        host="localhost",  # ou o endereço do servidor MySQL
        user="root",  # Seu user utilizado
        password="",  # Sua senha utilizada no banco de dados
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
    insert_if_not_exist = "INSERT INTO clients IF NOT EXIST values( %s, %s)"
    values = [
        ("test1", "test1@gmail.com"),
        ("test2", "test2@gmail.com"),
        ("test3", "test3@gmail.com"),
        ("test4", "test4@gmail.com"),
        ("test5", "test5@gmail.com"),
        ("test6", "test6@gmail.com"),
        ("test7", "test7@gmail.com"),
        ("test8", "test8@gmail.com"),
        ("test9", "test9@gmail.com"),
        ("test10", "test10@gmail.com"),
        ("test11", "test11@gmail.com"),
        ("test12", "test12@gmail.com"),
    ]
    mycursor.execute(insert_if_not_exist, values)
    # Commit as mudanças e fechar a conexão
    db.commit()


# ***********************************************************************************************************************#
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
# ***********************************************************************************************************************
# ESTILIZAÇÃO JANELA MAIN
janela_main.configure(bg="#CFD2CD")
clients_button.config(bg="#252627", fg="#fff")
email_button.config(bg="#252627", fg="#fff")
# Mantendo ela aberta
janela_main.mainloop()
