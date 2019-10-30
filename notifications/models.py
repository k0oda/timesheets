from django.db import models
from company_panel.models import Company
from django.conf import settings


class Invitation(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    def __str__(self):
        return self.target_user.username
