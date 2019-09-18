from django.db import models
from datetime import date


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())

    def __str__(self):
        return self.name

class Entry(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=date.today())
    project_id = models.BigIntegerField()
    task_id = models.BigIntegerField()
    notes = models.CharField(max_length=350, blank=True)
    timer = models.TimeField(default='0:00')

    def __str__(self):
        return self.name
