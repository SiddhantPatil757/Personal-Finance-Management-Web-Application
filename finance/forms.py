
from django import forms
from .models import Income
from .models import Goal
from .models import Expense
from .models import Budget
from .models import Saving

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'source', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'payment_mode', 'description']
        widgets = {
    'date': forms.DateInput(attrs={'type': 'date'})
}
        
class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = ['date', 'amount', 'description']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'Month'})
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['target_amount']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'})
        }