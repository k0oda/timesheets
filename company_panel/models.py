from django.db import models
from datetime import date
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='company_own')

    def __str__(self):
        return self.name

class Role(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    user_info_access = models.BooleanField()
    detailed_project_info_access = models.BooleanField()
    project_manage_access = models.BooleanField()
    invite_user_access = models.BooleanField()
    kick_user_access = models.BooleanField()
    expenses_manage_access = models.BooleanField()
    invoices_manage_access = models.BooleanField()
    client_manage_access = models.BooleanField()
    task_manage_access = models.BooleanField()
    expense_category_manage_access = models.BooleanField()

    def __str__(self):
        return self.name
