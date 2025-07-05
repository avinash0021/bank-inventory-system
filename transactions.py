# modules/transactions.py

def get_all_transactions(cursor):
    cursor.execute("SELECT * FROM transactions")
    return cursor.fetchall()

def add_transaction(cursor, account_id, amount, txn_type):
    if txn_type not in ('credit', 'debit'):
        raise ValueError("Transaction type must be 'credit' or 'debit'")

    cursor.execute("""
        INSERT INTO transactions (account_id, amount, type)
        VALUES (?, ?, ?)
    """, (account_id, amount, txn_type))
