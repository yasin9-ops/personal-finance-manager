import csv
from database import get_db

def backup_transactions(user_id, filename = "transactions_backup.csv"):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, category, amount, date FROM transactions WHERE user_id=? ", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "type", "category", "amount", "date"])
        writer.writerows(rows)

    print(f"Backup saved to {filename}")

def restore_transactions(user_id, filename = "transactions_backup.csv"):
    conn =get_db()
    cursor = conn.cursor()
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""INSERT INTO transactions (id, user_id, type, category, amount, date)
                VALUES (?, ?, ?, ?, ?, ?)""", (row["id"], user_id, row["type"], row["category"], float(row["amount"]), row["date"]))

    conn.commit()
    conn.close()
    print(f"Data restored from {filename}")