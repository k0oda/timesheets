from django.urls import path
from settings.views import Settings

urlpatterns = [
    path('', Settings.main, name='settings')
]