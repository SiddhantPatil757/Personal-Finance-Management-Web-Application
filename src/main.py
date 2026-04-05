from datetime import date
import mysql.connector

# ---------- MySQL Connection ----------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pune@123",
    database="finance_db"
)
cursor = conn.cursor()

# ---------- Constants ----------
INCOME_SOURCES = ["Salary", "Business", "Commission", "Bonus", "Other"]
CATEGORIES = ["Food", "Fuel", "Rent", "Bills", "Travel", "Shopping", "Healthcare", "Entertainment", "Other"]
PAYMENT_MODES = ["Cash", "UPI", "Credit Card", "Debit Card"]


class FinanceManager:

    def __init__(self):
        self.current_month = date.today().strftime("%Y-%m")

    # ---------- Utility ---------- #

    def get_positive_amount(self, prompt):
        while True:
            try:
                val = float(input(prompt))
                if val > 0:
                    return val
                else:
                    print("Amount must be positive.")
            except:
                print("Enter numeric value.")

    def get_selection(self, options):
        for i, item in enumerate(options, 1):
            print(f"{i}. {item}")
        while True:
            ch = input("Select number: ")
            if ch.isdigit() and 1 <= int(ch) <= len(options):
                return options[int(ch) - 1]
            print("Invalid selection.")

    # ---------- Core Functions ---------- #

    def add_income(self):
        source = self.get_selection(INCOME_SOURCES)
        amount = self.get_positive_amount("Enter Income Amount: ")
        today = date.today().isoformat()

        cursor.execute(
            "INSERT INTO income (date, source, amount) VALUES (%s, %s, %s)",
            (today, source, amount)
        )
        conn.commit()

        print("Income added successfully!")

    def allocate_budget(self):
        category = self.get_selection(CATEGORIES)
        amount = self.get_positive_amount("Enter Budget Amount: ")

        cursor.execute(
            "INSERT INTO budget (month, category, allocated_amount) VALUES (%s, %s, %s)",
            (self.current_month, category, amount)
        )
        conn.commit()

        print("Budget allocated successfully!")

    def add_saving(self):
        amount = self.get_positive_amount("Enter Saving Amount: ")
        today = date.today().isoformat()

        cursor.execute(
            "INSERT INTO savings (date, amount) VALUES (%s, %s)",
            (today, amount)
        )
        conn.commit()

        print("Saving recorded successfully!")

    def add_expense(self):
        category = self.get_selection(CATEGORIES)
        amount = self.get_positive_amount("Enter Expense Amount: ")
        payment_mode = self.get_selection(PAYMENT_MODES)
        description = input("Enter Description: ")
        today = date.today().isoformat()

        cursor.execute(
            """INSERT INTO expenses 
            (date, category, amount, payment_mode, description) 
            VALUES (%s, %s, %s, %s, %s)""",
            (today, category, amount, payment_mode, description)
        )
        conn.commit()

        print("Expense recorded successfully!")

    # ---------- Monthly Summary ---------- #

    def monthly_summary(self):
        month = self.current_month

        # Totals
        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM income WHERE DATE_FORMAT(date, '%Y-%m') = %s", (month,))
        total_income = cursor.fetchone()[0]

        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses WHERE DATE_FORMAT(date, '%Y-%m') = %s", (month,))
        total_expense = cursor.fetchone()[0]

        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM savings WHERE DATE_FORMAT(date, '%Y-%m') = %s", (month,))
        total_saving = cursor.fetchone()[0]

        net_balance = total_income - total_expense - total_saving

        print("\n====== Monthly Summary ======")
        print(f"Month: {month}")
        print(f"Income: {total_income}")
        print(f"Expense: {total_expense}")
        print(f"Saving: {total_saving}")
        print(f"Net Balance: {net_balance}")

        # Category Breakdown
        print("\n------ Category-wise Expense Breakdown ------")

        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE DATE_FORMAT(date, '%Y-%m') = %s
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (month,))

        categories = cursor.fetchall()
        total_expense_safe = total_expense if total_expense else 1

        for category, spent in categories:
            percent = (spent / total_expense_safe) * 100
            print(f"{category}: {spent} ({percent:.2f}%)")

        # Advanced Metrics
        print("\n------ Advanced Financial Metrics ------")

        if total_income > 0:
            expense_ratio = (total_expense / total_income) * 100
            saving_rate = (total_saving / total_income) * 100
        else:
            expense_ratio = 0
            saving_rate = 0

        print(f"Expense to Income Ratio: {expense_ratio:.2f}%")
        print(f"Savings Rate: {saving_rate:.2f}%")

        score = self.financial_health(total_income, total_expense, total_saving)
        print(f"Financial Health Score: {score}/100")

    # ---------- Financial Health ---------- #

    def financial_health(self, income, expense, saving):
        if income == 0:
            return 0

        saving_rate = saving / income
        expense_ratio = expense / income

        score = min(saving_rate * 50, 50)

        if expense_ratio <= 0.5:
            score += 30
        elif expense_ratio <= 0.7:
            score += 20
        else:
            score += 10

        if income - expense - saving > 0:
            score += 20

        return round(score, 2)


# ---------- Main ---------- #

def main():
    app = FinanceManager()

    while True:
        print("\n====== Personal Finance System ======")
        print("1. Add Income")
        print("2. Allocate Budget")
        print("3. Add Saving")
        print("4. Add Expense")
        print("5. Monthly Summary")
        print("6. Exit")

        ch = input("Select option: ")

        if ch == "1":
            app.add_income()
        elif ch == "2":
            app.allocate_budget()
        elif ch == "3":
            app.add_saving()
        elif ch == "4":
            app.add_expense()
        elif ch == "5":
            app.monthly_summary()
        elif ch == "6":
            break
        else:
            print("Invalid option.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
