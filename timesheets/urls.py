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
from timesheets_app.views import Main, CompanyPanel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.main, name='main'),
    path('login/', Authentication.login, name='login'),
    path('register/', Authentication.register, name='register'),
    path('exit', Authentication.exit, name='exit'),
    path('company/new', Main.new_company, name='new_company'),
    path('time/', CompanyPanel.time, name='time'),
    path('time/<int:year>/<int:month>/<int:day>/', CompanyPanel.time, name='time'),
    path('time/add/<int:year>/<int:month>/<int:day>/', CompanyPanel.add_entry, name='add_entry'),
    path('time/edit/<int:pk>/', CompanyPanel.edit_entry, name='edit_entry'),
    path('time/delete/<int:pk>/', CompanyPanel.delete_entry, name="delete_entry"),
    path('expenses/', CompanyPanel.expenses, name='expenses'),
    path('projects/', CompanyPanel.projects, name='projects'),
    path('team/', CompanyPanel.team, name='team'),
    path('invoices/', CompanyPanel.invoices, name='invoices'),
    path('manage/', CompanyPanel.manage, name='manage'),
    path('start/<int:entry_id>/', CompanyPanel.start_timer, name='start'),
    path('stop/<int:entry_id>/', CompanyPanel.stop_timer, name='stop')
]
