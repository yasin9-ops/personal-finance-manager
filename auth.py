import sqlite3
from database import get_db

def register_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("User already exists!")
    conn.close()

def login_user(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user
