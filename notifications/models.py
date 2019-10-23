from django.db import models
from company_panel.models import Company
from authentication.models import UserProfile


class Invitation(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    target_user = models.ForeignKey(UserProfile, models.CASCADE)

    def __str__(self):
        return self.target_user.name
