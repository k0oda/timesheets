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
