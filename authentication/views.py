from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import LoginForm, RegisterForm
from django.contrib import messages

def _login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Login or password is incorrect!')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'authentication/auth.html', {
        'form': form,
        'primary_value': 'Login',
        'secondary_link': 'register',
        'secondary_value': 'Create account',
        })

def _register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']

            if password == repeat_password:
                user = get_user_model().objects.create_user(
                    username, 
                    email=email, 
                    password=password, 
                    first_name=first_name, 
                    last_name=last_name
                    )
                user.save()
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Passwords do not match!')
                return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'authentication/auth.html', {
        'form': form,
        'primary_value': 'Create account',
        'secondary_link': 'login',
        'secondary_value': 'Login',
        })

def exit(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')
