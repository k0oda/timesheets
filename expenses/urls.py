from expenses.views import Expenses
from django.urls import path

urlpatterns = [
    path('', Expenses.expenses, name='expenses'),
    path('expenses/add/', Expenses.add_expense, name='add_expense'),
    path('expenses/edit/<int:expense_id>/', Expenses.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:expense_id>/', Expenses.delete_expense, name='delete_expense')
]
