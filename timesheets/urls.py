"""timesheets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication.views import Authentication
from company_panel.views import CompanyPanel
from times.views import Time
from expenses.views import Expenses
from projects.views import Projects
from team.views import Team
from invoices.views import Invoices
from manage_app.views import Manage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CompanyPanel.main, name='main'),
    path('login/', Authentication.login, name='login'),
    path('register/', Authentication.register, name='register'),
    path('exit', Authentication.exit, name='exit'),
    path('company/new', CompanyPanel.new_company, name='new_company'),
    path('time/', Time.time, name='time'),
    path('time/<int:year>/<int:month>/<int:day>/', Time.time, name='time'),
    path('time/add/<int:year>/<int:month>/<int:day>/', Time.add_entry, name='add_entry'),
    path('time/edit/<int:pk>/', Time.edit_entry, name='edit_entry'),
    path('time/delete/<int:pk>/', Time.delete_entry, name="delete_entry"),
    path('time/pick/', Time.pick_date, name='pick_date'),
    path('start/<int:entry_id>/', Time.start_timer, name='start'),
    path('stop/<int:entry_id>/', Time.stop_timer, name='stop'),
    path('expenses/', Expenses.expenses, name='expenses'),
    path('expenses/add/', Expenses.add_expense, name='add_expense'),
    path('expenses/edit/<int:expense_id>/', Expenses.edit_expense, name='edit_expense'),
    path('projects/', Projects.projects, name='projects'),
    path('team/', Team.team, name='team'),
    path('invoices/', Invoices.invoices, name='invoices'),
    path('manage/', Manage.manage, name='manage')
]
