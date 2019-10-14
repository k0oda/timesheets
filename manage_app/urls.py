from django.urls import path
from manage_app.views import Manage

urlpatterns = [
    path('', Manage.base, name='manage'),
    path('clients', Manage.clients, name='clients')
]