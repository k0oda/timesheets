from django.urls import path
from company_panel import views

urlpatterns = [
    path('company/edit/', views.edit_company, name='edit_company'),
    path('company/leave/', views.leave_company, name='leave_company'),
    path('company/new', views.new_company, name='new_company'),
    path('role/add/', views.add_role, name='add_role'),
    path('role/edit/<int:pk>/', views.edit_role, name='edit_role'),
    path('role/delete/<int:pk>/', views.delete_role, name='delete_role')
]
