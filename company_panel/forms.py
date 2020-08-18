from django import forms
from .models import Company, Role


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


class CreateRole(forms.ModelForm):
    def __init__(self, editable_object=None, *args, **kwargs):
        super(CreateRole, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            max_length=150,
            initial=editable_object.name if editable_object else None,
            label='Name'
        )
        self.fields['user_info_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.user_info_access if editable_object else None,
            required=False
        )
        self.fields['detailed_project_info_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.detailed_project_info_access if editable_object else None,
            required=False
        )
        self.fields['project_manage_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.project_manage_access if editable_object else None,
            required=False
        )
        self.fields['invite_user_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.invite_user_access if editable_object else None,
            required=False
        )
        self.fields['kick_user_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.kick_user_access if editable_object else None,
            required=False
        )
        self.fields['invoices_manage_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.invoices_manage_access if editable_object else None,
            required=False
        )
        self.fields['client_manage_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.client_manage_access if editable_object else None,
            required=False
        )
        self.fields['task_manage_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.task_manage_access if editable_object else None,
            required=False
        )
        self.fields['edit_company_info_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.edit_company_info_access if editable_object else None,
            required=False
        )
        self.fields['manage_roles_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.manage_roles_access if editable_object else None,
            required=False
        )
        self.fields['manage_hourly_rates_access'] = forms.BooleanField(
            widget=forms.CheckboxInput(),
            initial=editable_object.manage_hourly_rates_access if editable_object else None,
            required=False
        )
    
    class Meta:
        model = Role
        exclude = ['company']
