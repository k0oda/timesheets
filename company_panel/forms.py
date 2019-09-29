from django import forms
from .models import Company


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)
