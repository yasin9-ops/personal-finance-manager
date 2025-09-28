import sqlite3
from database import get_db

def init_transactions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT, -- "income" or "expense"
        category TEXT,
        amount REAL,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def add_transaction(user_id, t_type, category, amount, date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                   (user_id, t_type, category, amount, date))
    conn.commit()
    conn.close()
    print()

def get_transactions(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_transaction(transaction_id, new_category, new_amount, new_date):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions 
        SET category=?, amount=?, date=? 
        WHERE id=?
    """, (new_category, new_amount, new_date, transaction_id))
    conn.commit()
    conn.close()
    print("transaction updated successfully!")

def delete_transaction(transaction_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()
    print("transaction deleted successfully!")