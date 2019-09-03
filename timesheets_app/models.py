from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=timezone.now())

    def __str__(self):
        return self.name
