from django.db import models
from datetime import date
from authentication.models import UserProfile


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())
    owner = models.ForeignKey(UserProfile, models.CASCADE)

    def __str__(self):
        return self.name
