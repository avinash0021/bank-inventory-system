# modules/customers.py

def get_all_customers(cursor):
    cursor.execute("SELECT * FROM customers")
    return cursor.fetchall()

def add_customer(cursor, name, email, phone):
    cursor.execute("""
        INSERT INTO customers (name, email, phone)
        VALUES (?, ?, ?)
    """, (name, email, phone))
