from django.urls import path, include
from projects.views import Projects

urlpatterns = [
    path('', Projects.projects, name='projects'),
    path('add/', Projects.add_project, name='add_project'),
    path('edit/<int:pk>', Projects.edit_project, name='edit_project'),
    path('delete/<int:pk>', Projects.delete_project, name='delete_project'),
    path('project/<int:pk>/', Projects.project, name='project')
]