from company_panel.views import CompanyPanel
from django.urls import path

urlpatterns = [
    path('company/new', CompanyPanel.new_company, name='new_company')
]
