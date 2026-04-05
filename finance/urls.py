from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-income/', views.add_income, name='add_income'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-saving/', views.add_saving, name='add_saving'),
    path('set-goal/', views.set_goal, name='set_goal'),
    path('add-budget/', views.add_budget, name='add_budget'),
]