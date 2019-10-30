from django.db import models
from company_panel.models import Company
from projects.models import Project
from manage_app.models import Category

class Expense(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    project = models.ForeignKey(Project, models.CASCADE, related_name='+')
    category = models.ForeignKey(Category, models.CASCADE, related_name='+')
    notes = models.CharField(max_length=350, blank=True, default=' ')
    date = models.DateField(auto_now=True)
    amount = models.FloatField()

    def __str__(self):
        return self.project.name
