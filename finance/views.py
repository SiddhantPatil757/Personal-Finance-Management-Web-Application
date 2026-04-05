from django.shortcuts import render, redirect
from django.db.models import Sum
from datetime import datetime
from decimal import Decimal
from .models import Income, Expense, Saving, Budget, Goal
from .forms import IncomeForm, ExpenseForm, SavingForm, BudgetForm, GoalForm
from django.db.models import Sum


# 🔹 HOME DASHBOARD
def home(request):

    selected_month = request.GET.get('month')

    if selected_month:
        try:
            month_date = datetime.strptime(selected_month, "%Y-%m")
        except ValueError:
            month_date = datetime.today()
    else:
        month_date = datetime.today()

    year = month_date.year
    month = month_date.month

    # 🔹 Filter data
    incomes = Income.objects.filter(date__year=year, date__month=month)
    expenses = Expense.objects.filter(date__year=year, date__month=month)
    savings = Saving.objects.filter(date__year=year, date__month=month)

    budgets = Budget.objects.filter(month=month_date.strftime("%m/%Y"))

    # 🔹 Totals
    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_saving = savings.aggregate(total=Sum('amount'))['total'] or 0

    net_balance = total_income - total_expense - total_saving

    # 🔹 Expense Breakdown
    category_data = expenses.values('category').annotate(total=Sum('amount'))

    # 🔹 Budget vs Actual (FIXED)
    budget_data = []

    for b in budgets:
        total_spent = Expense.objects.filter(
            category=b.category,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        remaining = b.allocated_amount - total_spent

        percentage = (total_spent / b.allocated_amount) * 100 if b.allocated_amount > 0 else 0

        if percentage >= 100:
            status = "Over"
        elif percentage >= 80:
            status = "Near Limit"
        else:
            status = "Under"

        budget_data.append({
            'category': b.category,
            'budget': b.allocated_amount,
            'spent': total_spent,
            'remaining': remaining,
            'percentage': round(percentage, 2),
            'status': status,
        })

    # 🔹 Saving Goal
    goal = Goal.objects.first()
    goal_amount = goal.target_amount if goal else 0

    progress = 0
    if goal_amount > 0:
        progress = (total_saving / goal_amount) * 100

    # 🔹 Context
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'total_saving': total_saving,
        'net_balance': net_balance,
        'category_data': category_data,
        'budget_data': budget_data,   # ✅ correct variable
        'selected_month': month_date.strftime("%Y-%m"),
        'goal_amount': goal_amount,
        'progress': progress,
    }

    return render(request, 'home.html', context)


# 🔹 ADD INCOME
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})


# 🔹 ADD EXPENSE
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})


# 🔹 ADD SAVING
def add_saving(request):
    if request.method == "POST":
        form = SavingForm(request.POST)
        if form.is_valid():
            saving = form.save(commit=False)

            # Convert YYYY-MM → YYYY-MM-01
            month_value = request.POST.get('date')
            saving.date = datetime.strptime(month_value, "%Y-%m").date()

            saving.save()
            return redirect('home')
    else:
        form = SavingForm()

    return render(request, 'add_saving.html', {'form': form})


# 🔹 SET GOAL
def set_goal(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            Goal.objects.all().delete()  # keep only one goal
            form.save()
            return redirect('home')
    else:
        form = GoalForm()

    return render(request, 'set_goal.html', {'form': form})


# 🔹 ADD BUDGET
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)

            # 🔥 Convert 2026-04 → 04/2026
            raw_month = request.POST.get('month')
            dt = datetime.strptime(raw_month, "%Y-%m")
            budget.month = dt.strftime("%m/%Y")

            budget.save()
            return redirect('home')
    else:
        form = BudgetForm()

    return render(request, 'add_budget.html', {'form': form})