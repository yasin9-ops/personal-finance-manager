from database import get_db

def init_budget():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 category TEXT,
                 budget_limit REAL,
                 FOREIGN KEY(user_id) REFERENCES users(id))""")
    conn.commit()
    conn.close()


def set_budget(user_id, category, limit):
    conn =get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budgets WHERE user_id=? AND category=? ",(user_id, category))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE budgets SET budget_limit=? WHERE user_id=? AND category=?", (limit, user_id, category))
        print(f"Updated budget for {category} {limit}")

    else:
        cursor.execute("INSERT INTO budgets (user_id, category, budget_limit) VALUES (?, ?, ?)", (user_id, category, limit))
        print(f"Set new budget for {category} {limit}")

    conn.commit()
    conn.close()

def check_budget(user_id, category, month, year):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT budget_limit FROM budgets WHERE user_id=? AND category=?", (user_id, category))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return None, 0, 0
    budget_limit = result[0]
    cursor.execute("""SELECT SUM(amount) FROM transactions WHERE user_id=? AND category=? 
                   AND type='expense' AND strftime('%m', date)=? 
                   AND strftime('%Y', date)=? """, (user_id, category, f"{month:02d}", str(year)))
    total_spent = cursor.fetchone()[0] or 0
    conn.close()

    return budget_limit, total_spent, budget_limit - total_spent