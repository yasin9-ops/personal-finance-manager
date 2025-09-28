import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user
from transactions import add_transaction, get_transactions
from reports import monthly_report, yearly_report
from budget import set_budget, check_budget
from backup import backup_transactions, restore_transactions
import datetime

def open_dashboard(user_id):
    dashboard = tk.Toplevel()
    dashboard.title("Personal Finance Manager - Dashboard")

    def add_txn():
        t_type = simple_input("Enter type (income/expense):")
        category = simple_input("Enter category:")
        amount = float(simple_input("Enter amount:"))
        date = simple_input("Enter date (YYYY-MM-DD):") or str(datetime.date.today())
        add_transaction(user_id, t_type, category, amount, date)
        messagebox.showinfo("Success", "Transaction added!")

    def view_txns():
        records = get_transactions(user_id)
        if not records:
            messagebox.showinfo("Transactions", "No records found.")
        else:
            txns = "\n".join([f"{r[0]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}" for r in records])
            messagebox.showinfo("Transactions", txns)

    def reports():
        rep_win = tk.Toplevel()
        rep_win.title("Reports")

        def monthly():
            month = int(simple_input("Enter month (1-12):"))
            year = int(simple_input("Enter year (YYYY):"))
            income, expenses, savings = monthly_report(user_id, month, year)
            messagebox.showinfo("Monthly Report", f"📅 {month}/{year}\nIncome: {income}\nExpenses: {expenses}\nSavings: {savings}")

        def yearly():
            year = int(simple_input("Enter year (YYYY):"))
            income, expenses, savings = yearly_report(user_id, year)
            messagebox.showinfo("Yearly Report", f"📅 {year}\nIncome: {income}\nExpenses: {expenses}\nSavings: {savings}")

        tk.Label(rep_win, text="Choose Report Type").pack(pady=5)
        tk.Button(rep_win, text="Monthly Report", width=20, command=monthly).pack(pady=5)
        tk.Button(rep_win, text="Yearly Report", width=20, command=yearly).pack(pady=5)

    def budgeting():
        bud_win = tk.Toplevel()
        bud_win.title("Budgeting")

        def set_bud():
            category = simple_input("Enter category:")
            limit = float(simple_input("Enter monthly limit:"))
            set_budget(user_id, category, limit)
            messagebox.showinfo("Budget", f"Budget set for {category}: {limit}")

        def check_bud():
            category = simple_input("Enter category:")
            month = int(simple_input("Enter month (1-12):"))
            year = int(simple_input("Enter year (YYYY):"))
            budget_limit, total_spent, remaining = check_budget(user_id, category, month, year)
            if budget_limit is None:
                messagebox.showwarning("Budget", f"No budget set for {category}.")
            else:
                messagebox.showinfo("Budget", f"Budget for {category}: {budget_limit}\nSpent: {total_spent}\nRemaining: {remaining}")

        tk.Label(bud_win, text="Choose Budget Action").pack(pady=5)
        tk.Button(bud_win, text="Set Budget", width=20, command=set_bud).pack(pady=5)
        tk.Button(bud_win, text="Check Budget", width=20, command=check_bud).pack(pady=5)


    def backup():
        backup_transactions(user_id)
        messagebox.showinfo("Backup", "Backup saved to transactions_backup.csv")

    def restore():
        restore_transactions(user_id)
        messagebox.showinfo("Restore", "Data restored from transactions_backup.csv")

    def logout():
        messagebox.showinfo("Logout", "You have logged out.")
        dashboard.destroy()

    tk.Button(dashboard, text="Add Transaction", width=20, command=add_txn).pack(pady=5)
    tk.Button(dashboard, text="View Transactions", width=20, command=view_txns).pack(pady=5)
    tk.Button(dashboard, text="Reports", width=20, command=reports).pack(pady=5)
    tk.Button(dashboard, text="Budgeting", width=20, command=budgeting).pack(pady=5)
    tk.Button(dashboard, text="Backup", width=20, command=backup).pack(pady=5)
    tk.Button(dashboard, text="Restore", width=20, command=restore).pack(pady=5)
    tk.Button(dashboard, text="Logout", width=20, command=logout).pack(pady=5)

def simple_input(prompt):
    top = tk.Toplevel()
    top.title("Input")
    tk.Label(top, text=prompt).pack(padx=10, pady=5)
    entry = tk.Entry(top)
    entry.pack(padx=10, pady=5)

    value = {"data": None}
    def submit():
        value["data"] = entry.get()
        top.destroy()

    tk.Button(top, text="OK", command=submit).pack(pady=5)
    top.wait_window()
    return value["data"]


def login():
    username = entry_user.get()
    password = entry_pass.get()
    user = login_user(username, password)
    if user:
        messagebox.showinfo("Success", "Login successful! ")
        root.destroy()
        open_dashboard(user[0])
    else:
        messagebox.showerror("Error", "Invalid credentials! ")\
        
def register():
    username = entry_user.get()
    password = entry_pass.get()
    if username and password:
        register_user(username, password)
        messagebox.showinfo("Success", "Registration complete!")
    else:
        messagebox.showerror("Error", "Please enter both username and password!")

root = tk.Tk()
root.title("Personal Finance Manager - Login")

tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=5)

entry_user = tk.Entry(root)
entry_pass = tk.Entry(root, show="*")

entry_user.grid(row=0, column=1, padx=10, pady=5)
entry_pass.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Login", width=10, command=login).grid(row=2, column=0, pady=10)
tk.Button(root, text="Register", width=10, command=register).grid(row=2, column=1, pady=10)

root.mainloop()