from django import forms


class EditUser(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EditUser, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            max_length=150,
            initial=user.username,
            label='Username'
        )
        self.fields['first_name'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            max_length=150,
            initial=user.first_name,
            label='First name'
        )
        self.fields['last_name'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            max_length=150,
            initial=user.last_name,
            label='Last name'
        )
        self.fields['email'] = forms.EmailField(
            widget=forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            initial=user.email,
            label='Email'
        )

