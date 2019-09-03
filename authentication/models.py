from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    company_id = models.BigIntegerField(null=True)
