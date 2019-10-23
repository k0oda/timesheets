from django.urls import path
from notifications.views import Notifications

urlpatterns = [
    path('', Notifications.notifications, name='notifications')
]