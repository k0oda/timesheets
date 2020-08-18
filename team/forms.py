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


class EditUserRole(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EditUserRole, self).__init__(*args, **kwargs)
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


class EditUserHourlyRate(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EditUserHourlyRate, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['hourly_rate'] = forms.DecimalField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            label='Hourly rate',
            required=True,
            initial=user.hourly_rate if user else 0
        )
