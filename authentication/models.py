from django.db import models
from django.contrib.auth.models import AbstractUser
from company_panel.models import Company, Role


class UserProfile(AbstractUser):
    company = models.ForeignKey(Company, models.SET_NULL, null=True, related_name='+')
    role = models.ForeignKey(Role, models.SET_NULL, null=True, related_name='+')
    hourly_rate = models.DecimalField(default=0, max_digits=20, decimal_places=2)
