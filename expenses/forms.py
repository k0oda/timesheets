from django import forms
from .models import Expense
from projects.models import Project
from manage_app.models import Category


class CreateExpense(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateExpense, self).__init__(*args, **kwargs)
        use_required_attribute = True
        self.fields['project'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Project.objects.filter(company=user.company),
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
            )
        )
        self.fields['amount'] = forms.DecimalField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            required=True
        )

    class Meta:
        model = Expense
        fields = ('project', 'category', 'notes', 'amount')
