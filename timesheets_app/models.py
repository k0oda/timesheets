from django.db import models
from datetime import date


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=150)
    company_id = models.BigIntegerField()
    default_hourly_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=150)
    client = models.ForeignKey(Client, models.CASCADE)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.name

class Entry(models.Model):
    date = models.DateField(default=date.today())
    project = models.ForeignKey(Project, models.CASCADE, default=None)
    task = models.ForeignKey(Task, models.CASCADE, default=None)
    notes = models.CharField(max_length=350, blank=True)
    timer = models.TimeField(default='0:00')

    def __str__(self):
        return self.project.name