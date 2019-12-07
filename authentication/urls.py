from django.urls import path
from authentication import views

urlpatterns = [
    path('login/', views._login, name='login'),
    path('register/', views._register, name='register'),
    path('exit', views.exit, name='exit')
]
