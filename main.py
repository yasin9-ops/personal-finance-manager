from auth import register_user, login_user
from transactions import init_transactions, get_transactions, add_transaction, update_transaction, delete_transaction
from reports import monthly_report, yearly_report
from budget import init_budget, set_budget, check_budget
from backup import backup_transactions, restore_transactions
import datetime

def main():
    print("=== Personal Finance Manager ===")
    print("1. Register")
    print("2. Login")
    choice = input("Choose an option: ")

    if choice == "1" :
        username = input("Enter username :")
        password = input("Enter password :")
        register_user(username, password)
    elif choice == "2" :
        username = input("Enter username :")
        password = input("Enter password :")
        user = login_user(username, password)
        if user:
            print("Login successful!")
            init_transactions()
            while True:
                print("\n--- Transactions Menu ---")
                print("1. Add Transaction")
                print("2. View Transactions")
                print("3. Update Transaction")
                print("4. Delete Transaction")
                print("5. Reports")
                print("6. Budgeting")
                print("7. Backup & Restore")
                print("8. Logout")
                choice = input("Choose an option: ")
                if choice == "1":
                    t_type = input("Enter type (income/expense): ")
                    category = input("Enter category (Food, Rent, Salary, etc.): ")
                    amount = float(input("Enter amount: "))
                    date = input("Enter date (YYYY-MM-DD): ") or str(datetime.date.today())
                    add_transaction(user[0], t_type, category, amount, date)
                elif choice == "2":
                    records = get_transactions(user[0])
                    for r in records:
                        print(r)
                elif choice == "3":
                    t_id  = int(input("Enter transaction ID to update :"))
                    new_category = input("Enter new category :")
                    new_amount = float(input("Enter new amount :"))
                    new_date = input("Enter new date (YYYY-MM-DD) :")
                    update_transaction(t_id, new_category, new_amount, new_date)
                elif choice == "4":
                    t_id = int(input("Enter transaction ID to delete :"))
                    delete_transaction(t_id)
                elif choice == "5":
                    print("--- Reports menu ---")
                    print("1. Monthly report")
                    print("2. Yearly report")
                    print("3. Back")

                    r_choice = input("Enter your choice :")
                    if r_choice == "1":
                        month = int(input("Enter month (1-12) :"))
                        year = int(input("Enter year (YYYY) :"))
                        income, expenses, savings = monthly_report(user[0], month, year)
                        print(f"Report for {month}/{year}")
                        print(f"Income:  {income}")
                        print(f"Expenses: {expenses}")
                        print(f"Savings: {savings}")
                    elif r_choice == "2":
                        year = int(input("Enter year :"))
                        income, expenses, savings = yearly_report(user[0], year)
                        print(f"Report for {year}")
                        print(f"Income: {income}")
                        print(f"Expenses: {expenses}")
                        print(f"Savings: {savings}")
                    elif choice == "3":
                        continue

                elif choice == "6":
                    init_budget()
                    print("-- Budget Menu -- ")
                    print("1. Set budget")
                    print("2. Check budget")
                    print("3. Back")
                    b_choice = input("Enter your choice :")
                    if b_choice == "1":
                        category = input("Enter category :")
                        limit = float(input("Enter monthly limit :"))
                        set_budget(user[0], category, limit)
                    elif b_choice == "2":
                        category = input("Enter category :")
                        month = int(input("Enter month (1-12) :"))
                        year = int(input("Enter year (YYYY) :"))
                        budget_limit, total_spent, remaining = check_budget(user[0], category, month, year)
                        if budget_limit is None:
                            print(f"No budget set for {category}. ")

                        else:
                            print(f"Budget for {category}: {budget_limit}")
                            print(f"Spent: {total_spent}")
                            print(f"Remaining: {remaining}")
                    elif b_choice == "3":
                        continue

                elif choice == "7":
                    print("--- Backup & Restore Menu ---")
                    print("1. Backup Transactions")
                    print("2. Restore Transactions")
                    print("3. Back")
                    br_choice = input("Choose an option: ")
                    if br_choice == "1":
                        backup_transactions(user[0])
                    elif br_choice == "2":
                        restore_transactions(user[0])
                    elif br_choice == "3":
                        continue

                elif choice == "8":
                    print("Logged out successfully!")
                    break
        else:
            print("Invalid credentials! :")

if __name__ == "__main__" :
    main()