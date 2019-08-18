from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    login.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Login',
    })

    password.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Password'
    })

class RegisterForm(forms.Form):
    login = forms.CharField(min_length=3, max_length=20)
    email = forms.EmailField()
    first_name = forms.CharField(min_length=3, max_length=50)
    last_name = forms.CharField(min_length=3, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    login.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Login',
    })

    email.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Email'
    })

    first_name.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'First name',
    })

    last_name.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Last name',
    })

    password.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Password',
    })

    repeat_password.widget.attrs.update({
        'class': 'form-control',
        'placeholder': 'Repeat password',
    })

