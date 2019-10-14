from django.urls import path
from manage_app.views import Manage

urlpatterns = [
    path('', Manage.manage, name='manage')
]