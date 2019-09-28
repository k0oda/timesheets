from django import forms
from .models import Company


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)

class DatePicker(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='')
