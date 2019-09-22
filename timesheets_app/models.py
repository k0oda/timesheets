from django.db import models
from datetime import date, time


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())

    def __str__(self):
        return self.name

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

class Project(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    name = models.CharField(max_length=150)
    client = models.ForeignKey(Client, models.CASCADE)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return self.name

class Entry(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    date = models.DateField(default=date.today())
    project = models.ForeignKey(Project, models.CASCADE)
    task = models.ForeignKey(Task, models.CASCADE)
    notes = models.CharField(max_length=350, blank=True, default=' ')
    timer = models.TimeField(default=time(0, 0))
    start_time = models.TimeField(default=time(0, 0))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.project.name