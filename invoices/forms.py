from django import forms
from .models import Invoice, Item
from manage_app.models import Client
from projects.models import Project


class CreateInvoice(forms.ModelForm):
    def __init__(self, user, editable_object=None, *args, **kwargs):
        super(CreateInvoice, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['client'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Client.objects.filter(company=user.company),
            initial=editable_object.client if editable_object else None,
            required=True,
            label='Client'
        )
        self.fields['date'] = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                },
                format="%Y-%m-%d"
            ),
            initial=editable_object.date if editable_object else None,
            required=True,
            label='Date'
        )
        self.fields['notes'] = forms.CharField(
            widget = forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': '3',
                    'rows': '5',
                    'placeholder': 'Notes (optional)'
                }
            ),
            required=False,
            initial=editable_object.notes if editable_object else None
        )

    class Meta:
        model = Invoice
        fields = ('client', 'date', 'notes')


class CreateItem(forms.ModelForm):
    def __init__(self, user, editable_object=None, *args, **kwargs):
        super(CreateItem, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['project'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Project.objects.filter(company=user.company),
            initial=editable_object.project if editable_object else None,
            required=True,
            label='Project'
        )

    class Meta:
        model = Item
        fields = ('project',)
