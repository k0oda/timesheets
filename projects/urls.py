from django.urls import path, include
from projects.views import Projects

urlpatterns = [
    path('', Projects.projects, name='projects'),
    path('add/', Projects.add_project, name='add_project'),
    path('edit/<int:pk>', Projects.edit_project, name='edit_project')
]