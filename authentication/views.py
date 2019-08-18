from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import LoginForm


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
        return render(request, 'authentication/login.html', {'form': form})
