from django.urls import path, include
from projects import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('add/', views.add_project, name='add_project'),
    path('edit/<int:pk>', views.edit_project, name='edit_project'),
    path('delete/<int:pk>', views.delete_project, name='delete_project'),
    path('project/<int:pk>/', views.project, name='project')
]