from django import forms
from .models import Company


class CreateCompany(forms.ModelForm):
    def __init__(self, editable_object=None, *args, **kwargs):
        super(CreateCompany, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            max_length=150,
            initial=editable_object.name if editable_object else None,
            label='Company name'
        )
    
    class Meta:
        model = Company
        fields = ('name',)
