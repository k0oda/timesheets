from django.urls import path
from invoices.views import Invoices

urlpatterns = [
    path('', Invoices.invoices, name='invoices'),
    path('new/', Invoices.add_invoice, name='add_invoice'),
    path('new/items/<int:invoice_pk>', Invoices.add_item, name='add_item'),
    path('edit/items/<int:pk>/', Invoices.edit_item, name='edit_item'),
    path('delete/items/<int:pk>/', Invoices.delete_item, name='delete_item')
]