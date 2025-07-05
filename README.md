# Bank Inventory Management System

A comprehensive desktop application built using **Python**, **Tkinter**, and **SQLite** that helps manage bank-related inventory assets, customer data, sales records, accounts, and transactions. It includes user authentication, role-based access (admin/staff), PDF/CSV export, and a clean GUI interface.

## 🖥️ Features

- 🔐 **Login, Register & Password Reset** with hashed credentials
- 👥 **User Roles**: Admin & Staff
- 🏦 **Asset Management** with stock alerts
- 👤 **Customer Management** with contact info
- 💸 **Sales Module** with customer and asset linkage
- 🧾 **Account & Transaction Management**
- 📁 **Export to CSV/PDF**
- 🔍 **Search Functionality**
- 🧠 **Low Stock Alerts**
- 🎨 GUI designed using Tkinter with custom background image

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter** – for GUI
- **SQLite3** – for local database
- **Pillow (PIL)** – for image handling
- **ttk** – styled widgets
- **CSV/PDF libraries** – for export features
- **OS & datetime** – for file paths and timestamps

## 📁 Project Structure

```
BankInventorySystem/
├── main.py                  # Main application
├── assets/
│   └── login_bg.png         # Background image
├── db/
│   └── bank_inventory_final.db  # SQLite database (auto-created)
├── exports/                 # Auto-created folder for CSV exports
├── pdfs/                    # Auto-created folder for PDF exports
├── modules/
│   ├── assets.py
│   ├── customers.py
│   ├── sales.py
│   ├── accounts.py
│   └── transactions.py
├── gui_tabs/
│   ├── asset_tab_ui.py
│   ├── customer_tab_ui.py
│   ├── sales_tab_ui.py
│   ├── account_tab_ui.py
│   └── transaction_tab_ui.py
```

## ⚙️ How to Run

1. **Install dependencies** (if not already installed):

```bash
pip install pillow
```

2. **Run the application**:

```bash
python main.py
```

The database and folders for exports will be created automatically on first run.

## 🧪 Modules Overview

| Module       | Description |
|--------------|-------------|
| `assets`     | Add, update, delete bank assets. Includes stock threshold alerts. |
| `customers`  | Manage customer details (name, email, phone). |
| `sales`      | Link customers with asset purchases. Logs quantity and sale amount. |
| `accounts`   | Manage bank accounts (number, IFSC, holder). |
| `transactions` | Credit/Debit transactions linked to accounts. |
| `gui_tabs`   | UI layout for each tab in the main dashboard. |

## 🔒 User Roles

- **Admin**: Full access to all features and modules.
- **Staff**: Restricted access based on role handling (extendable).

## 📝 Future Enhancements

- Add **PDF export** capability per module
- Include **Charts/Dashboard Stats**
- Implement **Role-based UI restrictions**
- Add **Search, Sort & Filter**
- Enable **.exe packaging using PyInstaller**
- Improve **Responsiveness & UI polish**


## 🧑‍💻 Author

Developed by [AVINASH GAUTAM]

## 📄 License

This project is open-source and free to use.
