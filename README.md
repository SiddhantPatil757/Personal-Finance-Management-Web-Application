# Personal-Finance-Management-Web-Application


PERSONAL FINANCE MANAGEMENT WEB APPLICATION

==================================================

PROJECT DESCRIPTION:
This is a full-stack web application developed using Django that helps users manage their daily financial activities. The system allows users to track income, expenses, savings, and budgets, and provides a clear financial overview through a dashboard.

The main goal of this project is to improve financial awareness and decision-making.

==================================================

CORE FEATURES:

1. INCOME MANAGEMENT

* Add income details (amount, source, date)
* View total income summary

2. EXPENSE TRACKING

* Record expenses with categories like Food, Rent, Travel, etc.
* View total expenses
* Analyse spending behaviour

3. BUDGET MANAGEMENT

* Set monthly budget for different categories
* Compare actual expenses with budget
* Calculate percentage of budget used
* Display status (Under Budget / Over Budget)

4. SAVINGS TRACKING

* Add savings records
* Monitor savings growth over time

5. FINANCIAL GOALS

* Set financial goals (example: save ₹50,000)
* Track progress toward goals

6. DASHBOARD (WEB + POWER BI)

* Django Dashboard Displays:

  * Total Income
  * Total Expenses
  * Total Savings
  * Budget vs Actual comparison

* Power BI Dashboard:

  * Advanced visual reports
  * Spending trends analysis
  * Category-wise breakdown
  * Monthly financial insights

==================================================

TECHNOLOGIES USED:

Backend:

* Python
* Django Framework

Frontend:

* HTML
* CSS

Database:

* MySQL (Primary Database)

Analytics & Visualization:

* Power BI (Dashboard & Reporting)

==================================================

PROJECT STRUCTURE:

finance_project/
│
├── finance/                 (Main App)
│   ├── models.py            (Database tables)
│   ├── views.py             (Business logic)
│   ├── forms.py             (User input forms)
│   ├── templates/           (HTML files)
│   └── static/              (CSS, JS files)
│
├── finance_project/         (Project settings)
│   ├── settings.py
│   ├── urls.py
│
├── manage.py                (Django command file)

==================================================

PREREQUISITES:

* Python (3.8+)
* pip
* MySQL Server
* VS Code or any editor

==================================================

INSTALLATION & SETUP:

STEP 1: Open Project Folder

* Open in VS Code
* Open terminal (where manage.py exists)

---

STEP 2: Create Virtual Environment

> python -m venv django_env

---

STEP 3: Activate Virtual Environment
Windows:

> django_env\Scripts\activate

Mac/Linux:

> source django_env/bin/activate

---

STEP 4: Install Required Packages

> pip install django mysqlclient

---

STEP 5: Configure MySQL Database

* Open settings.py
* Update DATABASES:

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.mysql',
'NAME': 'finance_db',
'USER': 'root',
'PASSWORD': 'your_password',
'HOST': 'localhost',
'PORT': '3306',
}
}

---

STEP 6: Apply Migrations

> python manage.py makemigrations
> python manage.py migrate

---

STEP 7: Run Server

> python manage.py runserver

---

STEP 8: Open in Browser
[http://127.0.0.1:8000/]

==================================================

POWER BI USAGE:

* Connect Power BI to MySQL database
* Import financial tables
* Create dashboards for:

  * Expense trends
  * Income vs Expense
  * Category analysis

==================================================

COMMON ERRORS:

1. MySQL not connecting

* Check username/password
* Ensure MySQL service is running

2. Module error

> pip install mysqlclient

3. Migration issues

> python manage.py migrate

==================================================

AUTHOR:
Siddhant Patil

==================================================
