from django.db import models
from company_panel.models import Company


class Task(models.Model):
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['company', 'name']

    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    default_hourly_rate = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name


class Client(models.Model):
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['company', 'name']

    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expenses Categories'
        ordering = ['company', 'name']

    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
