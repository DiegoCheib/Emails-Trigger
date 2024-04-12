import tkinter as tk
from tkinter import ttk
import mysql.connector
import smtplib
from mailjet_rest import Client
from funcoes import *
import time


# ***********************************************************************************************************************#



# ***********************************************************************************************************************#


def database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        auth_plugin='mysql_native_password'
    )
    mycursor = db.cursor()

   # Obter a lista de todos os bancos de dados
    mycursor.execute("SHOW DATABASES")
    databases = [db[0] for db in mycursor.fetchall()]

    # Verificar se o banco de dados "emailstrigger" existe
    if "emailstrigger" not in databases:
        # Se não existir, criar o banco de dados
        mycursor.execute("CREATE DATABASE emailstrigger")

    time.sleep(1)
    
    # Reconectar ao novo banco de dados para usar
    db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="emailstrigger",
    auth_plugin='mysql_native_password'
    )
    mycursor = db.cursor()
    
    # Criar a tabela se não existir
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INT AUTO_INCREMENT PRIMARY KEY,
        clients_name VARCHAR(255),
        clients_email VARCHAR(255),
        triggered ENUM('Not Selected', 'Selected', 'Option 3')
        )
    """)

    
    # Inserir dados de teste
    mycursor.execute("""
    INSERT INTO emails (clients_name, clients_email, triggered) VALUES
    ('teste1','test1@example.com', 'Not Selected'),
    ('teste2','test2@example.com', 'Not Selected'),
    ('teste3','test3@example.com', 'Not Selected')
    """)
    
    db.commit()
    db.close()

#database()



# ***********************************************************************************************************************#

def main():
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
main()

