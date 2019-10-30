from django.db import models
from company_panel.models import Company
from manage_app.models import Client, Task


class Project(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    client = models.ForeignKey(Client, models.CASCADE, related_name='+')
    tasks = models.ManyToManyField(Task)
    notes = models.CharField(max_length=350, blank=True, default=' ')
    budget = models.FloatField()
    total_earned = models.FloatField(default=0)
    total_spent = models.FloatField(default=0)

    def __str__(self):
        return self.name
