from django.db import models
from django.contrib.auth.models import AbstractUser
from company_panel.models import Company


class UserProfile(AbstractUser):
    company = models.ForeignKey(Company, models.SET_NULL, null=True)
