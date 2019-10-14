from django.urls import path
from manage_app.views import Manage

urlpatterns = [
    path('', Manage.base, name='manage'),
    path('clients', Manage.clients, name='clients'),
    path('tasks', Manage.tasks, name='tasks'),
    path('expense_categories', Manage.expense_categories, name='expense_categories')
]