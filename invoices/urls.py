from django.urls import path
from invoices.views import Invoices

urlpatterns = [
    path('', Invoices.invoices, name='invoices'),
    path('new/', Invoices.add_invoice, name='add_invoice'),
]