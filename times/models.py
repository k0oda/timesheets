from django.db import models
from company_panel.models import Company
from authentication.models import UserProfile
from manage_app.models import Task
from projects.models import Project
from datetime import date, time


class Entry(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    user = models.ForeignKey(UserProfile, models.CASCADE)
    date = models.DateField(default=date.today())
    project = models.ForeignKey(Project, models.CASCADE)
    task = models.ForeignKey(Task, models.CASCADE)
    notes = models.CharField(max_length=350, blank=True, default=' ')
    timer = models.TimeField(default=time(0, 0))
    start_time = models.TimeField(default=time(0, 0))
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.project.name
