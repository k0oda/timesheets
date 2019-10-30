from django.db import models
from datetime import date
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='company_own')

    def __str__(self):
        return self.name
