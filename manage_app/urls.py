from django.urls import path
from manage_app import views

urlpatterns = [
    path('', views.manage, name='manage'),
    path('clients', views.clients, name='clients'),
    path('clients/new/', views.add_client, name='add_client'),
    path('clients/edit/<int:pk>/', views.edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', views.delete_client, name='delete_client'),
    path('tasks', views.tasks, name='tasks'),
    path('tasks/new/', views.add_task, name='add_task'),
    path('tasks/edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),
]