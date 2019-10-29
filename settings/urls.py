from django.urls import path
from settings.views import Settings

urlpatterns = [
    path('', Settings.main, name='settings'),
    path('user/', Settings.edit_user, name='edit_user')
]