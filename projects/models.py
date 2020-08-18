from django.db import models
from company_panel.models import Company
from manage_app.models import Client, Task


class Project(models.Model):
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['company', 'name']

    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    client = models.ForeignKey(Client, models.CASCADE, related_name='+')
    tasks = models.ManyToManyField(Task)
    notes = models.TextField(max_length=350, blank=True, default=' ')

    def __str__(self):
        return self.name
