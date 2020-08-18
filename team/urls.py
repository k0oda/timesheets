from django.urls import path
from team import views

urlpatterns = [
    path('', views.team, name='team'),
    path('invite/', views.invite, name='invite'),
    path('invite/accept/<int:pk>', views.accept_invitation, name='accept_invitation'),
    path('user/<int:pk>/', views.user_profile, name='user_profile'),
    path('user/kick/<int:pk>/', views.kick_user, name='kick_user'),
    path('user/<int:pk>/edit/role/', views.edit_user_role, name='edit_user_role'),
    path('user/<int:pk>/edit/hourly_rate/', views.edit_user_hourly_rate, name='edit_user_hourly_rate')
]
