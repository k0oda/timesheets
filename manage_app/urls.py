from django.urls import path
from manage_app.views import Manage

urlpatterns = [
    path('', Manage.base, name='manage'),
    path('clients', Manage.clients, name='clients'),
    path('clients/new/', Manage.add_client, name='add_client'),
    path('clients/edit/<int:pk>/', Manage.edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', Manage.delete_client, name='delete_client'),
    path('tasks', Manage.tasks, name='tasks'),
    path('tasks/new/', Manage.add_task, name='add_task'),
    path('tasks/edit/<int:pk>/', Manage.edit_task, name='edit_task'),
    path('tasks/delete/<int:pk>/', Manage.delete_task, name='delete_task'),
    path('expense_categories', Manage.expense_categories, name='expense_categories'),
    path('expense_categories/new/', Manage.add_category, name='add_expense_category'),
    path('expense_categories/edit/<int:pk>/', Manage.edit_category, name='edit_expense_category')
]