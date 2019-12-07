from django.urls import path
from invoices import views

urlpatterns = [
    path('', views.invoices, name='invoices'),
    path('new/', views.add_invoice, name='add_invoice'),
    path('edit/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    path('delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('new/items/<int:invoice_pk>', views.add_item, name='add_item'),
    path('edit/items/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete/items/<int:pk>/', views.delete_item, name='delete_item')
]