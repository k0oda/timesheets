from django.db import models
from company_panel.models import Company


class Task(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    name = models.CharField(max_length=150)
    default_hourly_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Client(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    name = models.CharField(max_length=150)
