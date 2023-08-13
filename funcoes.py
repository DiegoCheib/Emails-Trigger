import tkinter as tk
from tkinter import ttk
import mysql.connector
import smtplib
from mailjet_rest import Client


def connect_database():
    db = mysql.connector.connect(
        host="localhost",  # ou o endereço do servidor MySQL
        user="root",
        password="",
        database="emailstrigger",
    )
    mycursor = db.cursor()


def display_data(clients_table, mycursor):
    mycursor.execute("SELECT * FROM clients")
    users = mycursor.fetchall()

    for user in users:
        clients_table.insert("", "end", values=user + ("unchecked",))


def get_checked_items(checked_items, marked_items):
    for item_id in marked_items:
        email, name = get_email_and_name_by_id(item_id)
        checked_items.append({"email": email, "name": name})

    return checked_items


def get_email_and_name_by_id(item_id, clients_table):
    values = clients_table.item(item_id, "values")
    email = values[2]
    name = values[1]
    return email, name



def toggleCheck(event, clients_table, marked_items):
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



def limpar_campos(assunto_email_entry, texto_email):
    assunto_email_entry.delete("0", "end")
    texto_email.delete("1.0", "end")


def funcao_composta_email():
    API_Mailjet()
    limpar_campos()


def funcao_composta_add_client():
    add_data()
    limpar_campos()


def funcao_composta_remove_client():
    remove_client()
    limpar_campos()


def funcao_composta_update_client():
    update_data()
    limpar_campos()

def sumir_widgets_(self):
    self.destroy()
    update_label.destroy()
    update_button.destroy()