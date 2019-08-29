from django.db import models


class Company(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150)


class Employees(models.Model):
    company_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
