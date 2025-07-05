# modules/sales.py

def get_all_sales(cursor):
    cursor.execute("SELECT * FROM sales")
    return cursor.fetchall()

def add_sale(cursor, customer_id, asset_id, quantity):
    cursor.execute("SELECT quantity, value FROM assets WHERE id=?", (asset_id,))
    asset = cursor.fetchone()
    if not asset:
        raise ValueError("Asset not found")
    if asset[0] < quantity:
        raise ValueError("Insufficient stock")

    amount = asset[1] * quantity
    cursor.execute("""
        INSERT INTO sales (customer_id, asset_id, quantity, amount)
        VALUES (?, ?, ?, ?)
    """, (customer_id, asset_id, quantity, amount))
    cursor.execute("UPDATE assets SET quantity = quantity - ? WHERE id=?", (quantity, asset_id))
