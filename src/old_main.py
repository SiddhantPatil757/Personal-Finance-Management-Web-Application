
import csv
import os 
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR,"Data")

INCOME_FILE = os.path.join(DATA_DIR,"income.csv")
EXPENSE_FILE = os.path.join(DATA_DIR,"expenses.csv")
SAVING_FILE = os.path.join(DATA_DIR,"savings.csv")
BUDGET_FILE = os.path.join(DATA_DIR,"budget.csv")
GOAL_FILE = os.path.join(DATA_DIR,"goal.csv")

os.makedirs(DATA_DIR,exist_ok = True)

INCOME_SOURCES = [
    "Salary",
    "Business",
    "Commission",
    "Bonus",
    "Rental Income",
    "Stock Profit",
    "Dividends",
    "Interest",
    "Investment Return",
    "Tax Refund",
    "Cashback",
    "Refund",
    "Gift",
    "Sales of Old Items",
    "Other"
]

CATEGORIES = [
    "Food",
    "Fuel",
    "Rent",
    "Bills",
    "Travel",
    "Shopping",
    "Healthcare",
    "Entertainment",
    "Insurance",
    "Education",
    "Other"
]

PAYMENT_MODES = [
    "Cash",
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Wallet"
]

def create_file_if_not_exists(file_path,headers):
    if not os.path.exists(file_path):
        with open(file_path,mode="w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
create_file_if_not_exists(INCOME_FILE,["date","source","amount"])
create_file_if_not_exists(EXPENSE_FILE,["date","category","amount","payment_mode","description"])
create_file_if_not_exists(SAVING_FILE,["date","amount","description"])
create_file_if_not_exists(BUDGET_FILE,["month","category","allocated_amount"])
create_file_if_not_exists(GOAL_FILE,["target_amount"])


def show_list(option,title):
    print(f"\nSelect {title}:")
    for i, item in enumerate(option,start = 1):
        print(f"{i}.{item}")

def get_selection(option,title):
    while True:
        show_list(option,title)
        choice = input(f"Enter {title} Number:")

        if choice.isdigit() and 1 <= int(choice) <= len(option):
            return option[int(choice) - 1]
        else:
            print("Invalid Choice. Try again.")

def get_positve_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater then zero.")

        except ValueError:
            print("Invalid Inpute. Enter Numric Vlue.")

def add_income():
    today = date.today().isoformat()
    source = get_selection(INCOME_SOURCES,"Income Source")
    amount = get_positve_amount("Enter Income Amount:")

    with open (INCOME_FILE,mode = "a", newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([today,source,amount])
    print("Income added Successfully!")

def add_expense():

    select_month = input("Enter month (YYYY-MM) or press Enter for current month:")
    if select_month.strip() == "":
        today = date.today().isoformat()
        current_month = date.today().strftime("%Y-%m")
    else:
        today = select_month + "-01"
        current_month = select_month
    category = get_selection(CATEGORIES,"Category")
    amount = get_positve_amount("Enter Expense Amount: ")
    payment_mode = get_selection(PAYMENT_MODES,"Payment Mode")
    description = input("Enter Description (optional): ")

    # buget for category
    budget_amount = 0
    with open(BUDGET_FILE,mode="r",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["month"] == current_month and row["category"] == category:
                budget_amount = float(row["allocated_amount"])
    
    # calculate already spent
    spent_amount = 0
    with open (EXPENSE_FILE,mode="r",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"].startswith(current_month) and row["category"] == category:
                spent_amount += float(row["amount"])
    
    new_total = spent_amount + amount

    if budget_amount > 0 and new_total > budget_amount:
        print(f"\nWARNING: Budget Exceeded for {category}!")
        print(f"Budget:{budget_amount}")
        print(f"New Total : {new_total}")
        print(f"Exceeded by: {new_total - budget_amount}")
        
    with open(EXPENSE_FILE,mode = "a", newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([today,category,amount,payment_mode,description])
    print("Expense added Sucessfully!")


def add_saving():
    today = date.today().isoformat()
    amount = get_positve_amount("Enter Saving Amount: ")
    description = input("Enter Saving Description:")

    with open(SAVING_FILE,mode="a",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([today,amount,description])
    print("Saving added successfully!")

def category_budget():
    current_month = date.today().strftime("%Y-%m")
    print(f"\nAllocating Budget for {current_month}")

    category = get_selection(CATEGORIES,"Category")
    amount = get_positve_amount("Enter Budget Amount:")

    with open(BUDGET_FILE, mode="a", newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([current_month, category, amount])
    
    print("Budget allocate successfully!")
    input("\nPress Enter to return to menu...")

def set_savings_goal():
    target = get_positve_amount("Enter Saving Target Amount:")

    with open(GOAL_FILE,mode="w",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["target_amount"])
        writer.writerow([target])
    
    print("Savings goal set successfully!")
    return("Press Enter to return to menu...")

def main():
    while True:
        print("\n====== Personal Finance System ======")
        print("1. Add Income")
        print("2. Set Saving Goal")
        print("3. Allocate Budget")
        print("4. Add Expense")
        print("5. Add Saving")
        print("6. Monthly Summary")
        print("7. Export Monthly Report")
        print("8. Exit")

        choice = input("Select an option: ")

def main():
    while True:
        print("\n====== Personal Finance System ======")
        print("1. Add Income")
        print("2. Set Saving Goal")
        print("3. Allocate Budget")
        print("4. Add Expense")
        print("5. Add Saving")
        print("6. Monthly Summary")
        print("7. Export Monthly Report")
        print("8. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            add_income()
        elif choice == "2":
            set_savings_goal()
        elif choice == "3":
            category_budget()
        elif choice == "4":
            add_expense()
        elif choice == "5":
            add_saving()
        elif choice == "6":
            monthly_summary()
        elif choice == "7":
            export_monthly_report()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid Option. Please Select 1-8.")


def monthly_summary():

    current_month = date.today().strftime("%Y-%m")

    total_income = 0
    total_expense = 0
    total_saving = 0
    category_expense = {}
    category_budget = {}

    # -------- Income --------
    with open(INCOME_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"].startswith(current_month):
                total_income += float(row["amount"])

    # -------- Expense --------
    with open(EXPENSE_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"].startswith(current_month):
                amount = float(row["amount"])
                total_expense += amount

                category = row["category"]
                if category in category_expense:
                    category_expense[category] += amount
                else:
                    category_expense[category] = amount

    # -------- Budget --------
    with open(BUDGET_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["month"] == current_month:
                category_budget[row["category"]] = float(row["allocated_amount"])

    # -------- Saving --------
    with open(SAVING_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"].startswith(current_month):
                total_saving += float(row["amount"])

    net_balance = total_income - total_expense - total_saving

    goal_amount = 0
    with open(GOAL_FILE,mode="r",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            goal_amount = float(row["target_amount"])
    
    if goal_amount > 0:
        progress = (total_saving/goal_amount) * 100
        print("\nSaving Goal Progress:")
        print(f"Target:{goal_amount}")         
        print(f"Saved:{total_saving}")         
        print(f"Progress:{progress:.2f}%")         


    print("\n====== Monthly Financial Summary ======")
    print(f"Month: {current_month}")
    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Total Saving: {total_saving}")
    print(f"Net Balance: {net_balance}")

    if total_income > 0:
        ratio = (total_expense / total_income) * 100
        print(f"Expense to Income Ratio: {ratio:.2f}%")
    else:
        print("Expense to Income Ratio: N/A")

    print("\nExpense Breakdown by Category:")
    if category_expense:
        for cat, amt in category_expense.items():
            print(f"{cat:<15}: {amt}")
    else:
        print("No expenses recorded this month.")

    print("\nBudget vs Actual:")
    if category_budget:
        for cat, budget in category_budget.items():
            spent = category_expense.get(cat, 0)

            print(f"\nCategory: {cat}")
            print(f"Budget : {budget}")
            print(f"Spent  : {spent}")

            if spent > budget:
                print(f"⚠ Exceeded by {spent - budget}")
            else:
                print(f"Remaining: {budget - spent}")
    else:
        print("No budget allocated for this month.")
    choice = input("\nDo you want to export this report? (Y/N): ")

    if choice.lower() == "y":
        export_monthly_report()
        
    input("\nPress Enter to return to menu...")



def export_monthly_report():
    month = input("Enter month (YYYY-MM): ")

    report_file = os.path.join(DATA_DIR, f"summary_{month}.csv")

    with open(report_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Month", "Income", "Expense", "Saving", "Net Balance"])

        # Recalculate for selected month
        total_income = total_expense = total_saving = 0

        with open(INCOME_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"].startswith(month):
                    total_income += float(row["amount"])

        with open(EXPENSE_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"].startswith(month):
                    total_expense += float(row["amount"])

        with open(SAVING_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"].startswith(month):
                    total_saving += float(row["amount"])

        net_balance = total_income - total_expense - total_saving

        writer.writerow([month, total_income, total_expense, total_saving, net_balance])

    print(f"Report exported to {report_file}")

    input("\nPress Enter to return to menu...")

if __name__ == "__main__":
    main()
    
   