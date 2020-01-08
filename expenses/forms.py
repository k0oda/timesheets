from django import forms
from .models import Expense
from projects.models import Project
from manage_app.models import Category


class CreateExpense(forms.ModelForm):
    def __init__(self, user, editable_object=None, *args, **kwargs):
        super(CreateExpense, self).__init__(*args, **kwargs)
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
        self.fields['category'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Category.objects.filter(company=user.company),
            initial=editable_object.category if editable_object else None,
            required=True,
            label='Category'
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
        self.fields['amount'] = forms.DecimalField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            initial=editable_object.amount if editable_object else None,
            required=True
        )

    class Meta:
        model = Expense
        fields = ('project', 'category', 'notes', 'amount')
