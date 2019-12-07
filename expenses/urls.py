from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.expenses, name='expenses'),
    path('expenses/add/', views.add_expense, name='add_expense'),
    path('expenses/edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:expense_id>/', views.delete_expense, name='delete_expense')
]
