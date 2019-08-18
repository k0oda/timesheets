from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(min_length=3, max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    login.widget.attrs.update({
        'class': 'form-control',
    })

    password.widget.attrs.update({
        'class': 'form-control',
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
    })

    email.widget.attrs.update({
        'class': 'form-control',
    })

    first_name.widget.attrs.update({
        'class': 'form-control',
    })

    last_name.widget.attrs.update({
        'class': 'form-control',
    })

    password.widget.attrs.update({
        'class': 'form-control',
    })

    repeat_password.widget.attrs.update({
        'class': 'form-control',
    })

