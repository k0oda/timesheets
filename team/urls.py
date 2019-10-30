from django.urls import path
from team.views import Team

urlpatterns = [
    path('', Team.team, name='team'),
    path('invite/', Team.invite, name='invite'),
    path('invite/accept/<int:pk>', Team.accept_invitation, name='accept_invitation'),
    path('user/<int:pk>/', Team.user_profile, name='user_profile'),
    path('user/kick/<int:pk>/', Team.kick_user, name='kick_user')
]
