from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


class Authentication:
    @staticmethod
    def login(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['login']
                password = form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    return redirect('/')
                else:
                    return redirect('/login/')  # TODO: Add authentication error page
        else:
            form = LoginForm()
        return render(request, 'authentication/auth.html', {
            'form': form,
            'primary_value': 'Login',
            'secondary_link': 'register',
            'secondary_value': 'Create account',
            })

    @staticmethod
    def register(request):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                login = form.cleaned_data['login']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                password = form.cleaned_data['password']
                repeat_password = form.cleaned_data['repeat_password']

                if password == repeat_password:
                    user = User.objects.create_user(
                        login, 
                        email=email, 
                        password=password, 
                        first_name=first_name, 
                        last_name=last_name
                        )
                    user.save()
                    return redirect('/')
                else:
                    return redirect('/login/')  # TODO: Add registration error page
        else:
            form = RegisterForm()
        return render(request, 'authentication/auth.html', {
            'form': form,
            'primary_value': 'Create account',
            'secondary_link': 'login',
            'secondary_value': 'Login',
            })

