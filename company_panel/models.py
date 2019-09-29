from django.db import models
from datetime import date


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())

    def __str__(self):
        return self.name
