# modules/accounts.py

def get_all_accounts(cursor):
    cursor.execute("SELECT * FROM accounts")
    return cursor.fetchall()

def add_account(cursor, acc_number, ifsc, holder):
    cursor.execute("""
        INSERT INTO accounts (account_number, ifsc_code, holder_name)
        VALUES (?, ?, ?)
    """, (acc_number, ifsc, holder))
