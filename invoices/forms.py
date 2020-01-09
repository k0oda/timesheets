from django import forms
from .models import Invoice, Item
from manage_app.models import Client


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
            initial=editable_object.notes if editable_object else None
        )

    class Meta:
        model = Invoice
        fields = ('client', 'date', 'notes')


class CreateItem(forms.ModelForm):
    def __init__(self, editable_object=None, *args, **kwargs):
        super(CreateItem, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['name'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            max_length=150,
            label='Name',
            required=True,
            initial=editable_object.name if editable_object else None
        )
        self.fields['description'] = forms.CharField(
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': '3',
                    'rows': '5',
                    'placeholder': 'Description (optional)'
                }
            ),
            max_length=350,
            required=False,
            initial=editable_object.description if editable_object else None
        )
        self.fields['amount'] = forms.IntegerField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Amount'
                }
            ),
            min_value=0,
            required=True,
            initial=editable_object.amount if editable_object else None
        )
        self.fields['unit_price'] = forms.DecimalField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Unit price'
                }
            ),
            required=True,
            initial=editable_object.unit_price if editable_object else None
        )

    class Meta:
        model = Item
        fields = ('name', 'amount', 'unit_price', 'description')
