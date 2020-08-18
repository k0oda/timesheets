"""timesheets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from company_panel.views import company as main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('auth/', include('authentication.urls')),
    path('company/', include('company_panel.urls')),
    path('time/', include('times.urls')),
    path('projects/', include('projects.urls')),
    path('team/', include('team.urls')),
    path('invoices/', include('invoices.urls')),
    path('manage/', include('manage_app.urls')),
    path('notifications/', include('notifications.urls')),
    path('settings/', include('settings.urls'))
]
