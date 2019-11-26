from company_panel.views import CompanyPanel
from django.urls import path

urlpatterns = [
    path('company/edit/', CompanyPanel.edit_company, name='edit_company'),
    path('company/leave/', CompanyPanel.leave_company, name='leave_company'),
    path('company/new', CompanyPanel.new_company, name='new_company'),
    path('role/add/', CompanyPanel.add_role, name='add_role'),
    path('role/edit/<int:pk>/', CompanyPanel.edit_role, name='edit_role'),
    path('role/delete/<int:pk>/', CompanyPanel.delete_role, name='delete_role')
]
