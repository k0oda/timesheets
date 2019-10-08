from authentication.views import Authentication
from django.urls import path

urlpatterns = [
    path('login/', Authentication.login, name='login'),
    path('register/', Authentication.register, name='register'),
    path('exit', Authentication.exit, name='exit')
]
