from django.urls import path
from settings.views import Settings
from company_panel.views import CompanyPanel

urlpatterns = [
    path('', Settings.main, name='settings'),
    path('user/', Settings.edit_user, name='edit_user'),
    path('user/password/', Settings.change_password, name='change_password'),
    path('company/', Settings.edit_company, name='edit_company'),
    path('company/leave/', Settings.leave_company, name='leave_company'),
    path('role/add/', CompanyPanel.add_role, name='add_role')
]