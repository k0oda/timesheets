from django import forms
from .models import Company


class CreateCompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Company name'})
    
    class Meta:
        model = Company
        fields = ('name',)
