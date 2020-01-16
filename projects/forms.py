from django import forms
from .models import Project
from manage_app.models import Client, Task


class CreateProject(forms.ModelForm):
    def __init__(self, user, editable_object=None, *args, **kwargs):
        super(CreateProject, self).__init__(*args, **kwargs)
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
        self.fields['client'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Client.objects.filter(company=user.company),
            required=True,
            initial=editable_object.client if editable_object else None,
            label='Client'
        )
        self.fields['tasks'] = forms.ModelMultipleChoiceField(
            widget=forms.SelectMultiple(
                attrs={
                    'class': 'form-control'
                }
            ),
            queryset=Task.objects.filter(company=user.company),
            required=True,
            initial=editable_object.tasks.all() if editable_object else None,
            label='Tasks'
        )
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Notes (optional)',
                    'cols': '3',
                    'rows': '5'
                }
            ),
            required=False,
            initial=editable_object.notes if editable_object else None
        )
        self.fields['budget'] = forms.DecimalField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Budget'
                }
            ),
            initial=editable_object.budget if editable_object else None,
            required=True
        )

    class Meta:
        model = Project
        fields = ('name', 'client', 'tasks', 'notes', 'budget')
