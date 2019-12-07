from django.db import models
from company_panel.models import Company
from manage_app.models import Client, Task


class Project(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    client = models.ForeignKey(Client, models.CASCADE, related_name='+')
    tasks = models.ManyToManyField(Task)
    notes = models.TextField(max_length=350, blank=True, default=' ')
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    total_earned = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    total_spent = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    def __str__(self):
        return self.name
