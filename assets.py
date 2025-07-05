# modules/assets.py

def get_all_assets(cursor):
    cursor.execute("SELECT * FROM assets")
    return cursor.fetchall()

def add_asset(cursor, name, category, quantity, value, threshold=5):
    cursor.execute("""
        INSERT INTO assets (name, category, quantity, value, low_stock_threshold)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, quantity, value, threshold))

def get_low_stock(cursor):
    cursor.execute("SELECT * FROM assets WHERE quantity <= low_stock_threshold")
    return cursor.fetchall()
