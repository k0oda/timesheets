from django.urls import path
from settings import views

urlpatterns = [
    path('', views.settings, name='settings'),
    path('user/', views.edit_user, name='edit_user'),
    path('user/password/', views.change_password, name='change_password')
]