from django.urls import path
from team.views import Team

urlpatterns = [
    path('', Team.team, name='team'),
    path('invite/', Team.invite, name='invite')
]
