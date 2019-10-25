from django.db import models
from manage_app.models import Client


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=350, blank=True)
    amount = models.FloatField()

    def __str__(self):
        return self.name


class Invoice(models.Model):
    client = models.ForeignKey(Client, models.CASCADE)
    date = models.DateField(auto_now=True)
    items = models.ManyToManyField(Item)
    notes = models.CharField(max_length=350, blank=True)

    def __str__(self):
        return self.client
