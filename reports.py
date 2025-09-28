from database import get_db

def monthly_report(user_id, month, year):
    conn = get_db()
    cursor = conn.cursor()
    conn.execute("SELECT type, amount FROM transactions WHERE user_id=? AND strftime('%m', date)=? AND strftime('%Y', date)=?", (user_id, f"{month:02d}", str(year)))
    rows = cursor.fetchall()
    conn.close()

    income = sum(r[1] for r in rows if r[0].lower() == "income")
    expenses = sum(r[1] for r in rows if r[0].lower() == "expense")
    savings = income - expenses
    return income, expenses, savings

def yearly_report(user_id, year):
    conn =get_db()
    cursor = conn.cursor()
    conn.execute("SELECT type, amount FROM transactions WHERE user_id=? AND strftime('%Y', date)=?", (user_id, str(year)))
    rows = cursor.fetchall()
    conn.close()

    income = sum(r[1] for r in rows if r[0].lower() == "income")
    expenses = sum(r[1] for r in rows if r[0].lower() == "expense")
    savings = income - expenses
    return income, expenses, savings