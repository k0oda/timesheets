from django.contrib import admin
from .models import Company, Entry, Client, Project, Task

admin.site.register(Company)
admin.site.register(Entry)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Task)
