
import tkinter as tk
from tkinter import ttk, messagebox
from modules import assets

def asset_tab_ui(app):
    frame = tk.Frame(app)

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Category", "Qty", "Value"), show="headings")
    for col in ("ID", "Name", "Category", "Qty", "Value"):
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    def refresh_tree():
        for i in tree.get_children():
            tree.delete(i)
        for row in assets.get_all_assets(app.cursor):
            tree.insert("", "end", values=row)

    def add_asset():
        name = name_entry.get()
        cat = category_entry.get()
        try:
            qty = int(quantity_entry.get())
            val = float(value_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid quantity and value")
            return

        assets.add_asset(app.cursor, name, cat, qty, val)
        app.conn.commit()
        refresh_tree()

    # Entry fields
    form = tk.Frame(frame)
    tk.Label(form, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1)
    tk.Label(form, text="Category").grid(row=1, column=0)
    category_entry = tk.Entry(form)
    category_entry.grid(row=1, column=1)
    tk.Label(form, text="Qty").grid(row=2, column=0)
    quantity_entry = tk.Entry(form)
    quantity_entry.grid(row=2, column=1)
    tk.Label(form, text="Value").grid(row=3, column=0)
    value_entry = tk.Entry(form)
    value_entry.grid(row=3, column=1)

    tk.Button(form, text="Add Asset", command=add_asset).grid(row=4, columnspan=2, pady=10)
    form.pack(pady=10)

    refresh_tree()
    return frame
