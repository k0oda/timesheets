from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from company_panel.models import Role
from .forms import EditUser, ChangePassword

@login_required
def settings(request):
    roles = Role.objects.filter(company=request.user.company)
    return render(request, 'settings/settings.html', context={
        'roles': roles
    })

@login_required
def edit_user(request):
    if request.method.lower() == 'post':
        form = EditUser(request.user, data=request.POST)
        if form.is_valid():
            request.user.username = form.cleaned_data['username']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
    return redirect('settings')

@login_required
def change_password(request):
    if request.method.lower() == 'post':
        form = ChangePassword(data=request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            new_password_repeat = form.cleaned_data['new_password_repeat']
            
            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                if new_password == new_password_repeat:
                    request.user.set_password(new_password)
                    request.user.save()
    return redirect('settings')
