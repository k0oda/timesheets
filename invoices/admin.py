from django.contrib import admin
from invoices.models import Item, Invoice

admin.site.register(Item)
admin.site.register(Invoice)
