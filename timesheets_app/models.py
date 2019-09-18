from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=timezone.now())

    def __str__(self):
        return self.name

class Entry(models.Model):
    name = models.CharField(max_length=100)
    project_id = models.BigIntegerField()
    task_id = models.BigIntegerField()
    notes = models.CharField(max_length=350, blank=True)
    timer = models.TimeField(blank=True)

    def __str__(self):
        return self.name
