
import tkinter as tk
from tkinter import ttk, messagebox
from modules import customers

def customer_tab_ui(app):
    frame = tk.Frame(app)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Email", "Phone"), show="headings")
    for col in ("ID", "Name", "Email", "Phone"):
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    def refresh_tree():
        for i in tree.get_children():
            tree.delete(i)
        for row in customers.get_all_customers(app.cursor):
            tree.insert("", "end", values=row)

    def add_customer():
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        customers.add_customer(app.cursor, name, email, phone)
        app.conn.commit()
        refresh_tree()

    form = tk.Frame(frame)
    tk.Label(form, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1)
    tk.Label(form, text="Email").grid(row=1, column=0)
    email_entry = tk.Entry(form)
    email_entry.grid(row=1, column=1)
    tk.Label(form, text="Phone").grid(row=2, column=0)
    phone_entry = tk.Entry(form)
    phone_entry.grid(row=2, column=1)

    tk.Button(form, text="Add Customer", command=add_customer).grid(row=3, columnspan=2, pady=10)
    form.pack(pady=10)

    refresh_tree()
    return frame
