# gui_tabs/sales_tab_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from modules import sales, customers, assets

def sales_tab_ui(app):
    frame = tk.Frame(app)

    def refresh_sales():
        for i in sales_tree.get_children():
            sales_tree.delete(i)
        for row in sales.get_all_sales(app.cursor):
            sales_tree.insert("", "end", values=row)

    def make_sale():
        try:
            customer_id = int(customer_entry.get())
            asset_id = int(asset_entry.get())
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            return
        try:
            sales.add_sale(app.cursor, customer_id, asset_id, quantity)
            app.conn.commit()
            messagebox.showinfo("Success", "Sale recorded")
            refresh_sales()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Form Inputs
    tk.Label(frame, text="Customer ID").grid(row=0, column=0, padx=5, pady=5)
    customer_entry = tk.Entry(frame)
    customer_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Asset ID").grid(row=1, column=0, padx=5, pady=5)
    asset_entry = tk.Entry(frame)
    asset_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
    quantity_entry = tk.Entry(frame)
    quantity_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(frame, text="Record Sale", command=make_sale).grid(row=3, column=0, columnspan=2, pady=10)

    # Sales Table
    sales_tree = ttk.Treeview(frame, columns=("ID", "CustID", "AssetID", "Qty", "Amount", "Date"), show="headings")
    for col in sales_tree["columns"]:
        sales_tree.heading(col, text=col)
        sales_tree.column(col, width=100)
    sales_tree.grid(row=4, column=0, columnspan=2, pady=10)

    refresh_sales()
    return frame