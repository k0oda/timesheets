from django import forms
from company_panel.models import Role


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


class EditUser(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EditUser, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['role'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Role.objects.filter(company=user.company),
            initial=user.role,
            label='Role',
            required=True
        )
