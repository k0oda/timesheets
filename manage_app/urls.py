from django.urls import path
from manage_app.views import Manage

urlpatterns = [
    path('', Manage.base, name='manage'),
    path('clients', Manage.clients, name='clients'),
    path('clients/new/', Manage.add_client, name='add_client'),
    path('clients/edit/<int:pk>/', Manage.edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', Manage.delete_client, name='delete_client'),
    path('tasks', Manage.tasks, name='tasks'),
    path('expense_categories', Manage.expense_categories, name='expense_categories')
]