from django import forms


class InviteUser(forms.Form):
    def __init__(self, *args, **kwargs):
        super(InviteUser, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['username'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            label='Username'
        )

