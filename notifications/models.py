from django.db import models
from company_panel.models import Company
from django.conf import settings


class Invitation(models.Model):
    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='+')

    def __str__(self):
        return self.target_user.username
