from django.db import models
from manage_app.models import Client
from company_panel.models import Company


class Item(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=350, blank=True)
    amount = models.FloatField()

    def __str__(self):
        return self.name


class Invoice(models.Model):
    client = models.ForeignKey(Client, models.CASCADE)
    company = models.ForeignKey(Company, models.CASCADE)
    date = models.DateField(auto_now=True)
    items = models.ManyToManyField(Item)
    notes = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return self.client
