from django.db import models
from manage_app.models import Client
from company_panel.models import Company


class Invoice(models.Model):
    client = models.ForeignKey(Client, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
    date = models.DateField(auto_now=True)
    total_amount = models.IntegerField(null=True, default=0)
    total_unit_price = models.FloatField(null=True, default=0)
    total_price = models.FloatField(null=True, default=0)
    notes = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return self.client.name

    def get_items(self):
        return Item.objects.filter(invoice=self)


class Item(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    invoice = models.ForeignKey(Invoice, models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=350, blank=True)
    unit_price = models.FloatField(default=0.0)
    amount = models.IntegerField(default=0)
    total_price = models.FloatField(null=True, default=0)

    def __str__(self):
        return self.name
