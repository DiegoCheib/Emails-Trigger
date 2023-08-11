import tkinter as tk
from tkinter import ttk

def toggle_checkbox(event):
    item = tree.identify_row(event.y)
    checked = tree.item(item, 'values')[0]
    tree.item(item, values=[not checked])

janela = tk.Tk()
janela.title("Checkbox dentro de Treeview")

tree = ttk.Treeview(janela, columns=("Checkbox", "Data"))
tree.heading("#0", text="Item")
tree.heading("Checkbox", text="Checkbox")
tree.heading("Data", text="Data")

tree.column("#0", width=100)
tree.column("Checkbox", width=50)
tree.column("Data", width=100)

tree.insert("", "end", text="Item 1", values=[True, "Data 1"])
tree.insert("", "end", text="Item 2", values=[False, "Data 2"])

tree.bind("<Button-1>", toggle_checkbox)

janela.mainloop()
