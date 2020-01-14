from django import forms
from .models import Task
from projects.models import Project
from manage_app.models import Category


class CreateTask(forms.ModelForm):
    def __init__(self, editable_object=None, *args, **kwargs):
        super(CreateTask, self).__init__(*args, **kwargs)
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
        self.fields['default_hourly_rate'] = forms.DecimalField(
            widget=forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            label='Default hourly rate',
            required=True,
            initial=editable_object.default_hourly_rate if editable_object else None
        )

    class Meta:
        model = Task
        fields = ('name', 'default_hourly_rate')
