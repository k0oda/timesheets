from django.db import models
from datetime import date
from django.conf import settings


class Company(models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['date_of_creation']

    name = models.CharField(max_length=150)
    date_of_creation = models.DateField(default=date.today())
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='company_own')

    def __str__(self):
        return self.name


class Role(models.Model):
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['company', 'name']

    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    name = models.CharField(max_length=150)
    user_info_access = models.BooleanField(default=False)
    detailed_project_info_access = models.BooleanField(default=False)
    project_manage_access = models.BooleanField(default=False)
    invite_user_access = models.BooleanField(default=False)
    kick_user_access = models.BooleanField(default=False)
    invoices_manage_access = models.BooleanField(default=False)
    client_manage_access = models.BooleanField(default=False)
    task_manage_access = models.BooleanField(default=False)
    edit_company_info_access = models.BooleanField(default=False)
    manage_roles_access = models.BooleanField(default=False)
    manage_hourly_rates_access = models.BooleanField(default=False)

    def __str__(self):
        return self.name
