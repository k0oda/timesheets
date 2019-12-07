from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from company_panel.models import Company, Role
from company_panel.forms import CreateCompanyForm

CHECKBOX_MAPPING = {
    'on': True,
    None: False
}

def company(request):
    if request.user.is_authenticated:
        return redirect('time')
    else:
        return render(request, 'company_panel/unauthenticated.html')

@login_required
def new_company(request):
    if request.method.lower() == 'post':
        form = CreateCompanyForm(request.POST)
        company = form.save(commit=False)
        user = request.user
        company.owner = user
        company.save()
        role = Role.objects.create(
            company=company,
            name='Owner',
            user_info_access=True,
            detailed_project_info_access=True,
            project_manage_access=True,
            invite_user_access=True,
            kick_user_access=True,
            expenses_manage_access=True,
            invoices_manage_access=True,
            client_manage_access=True,
            task_manage_access=True,
            expense_category_manage_access=True,
            edit_company_info_access=True,
            manage_roles_access=True
        )
        role.save()
        user.company = company
        user.role = role
        user.save()
        return redirect('/')
    else:
        form = CreateCompanyForm()
    return render(request, 'company_panel/new_company.html', {'form': form})

@login_required
def edit_company(request):
    if request.user.role.edit_company_info_access:
        if request.method.lower() == 'post':
            request.user.company.name = request.POST.get('name')
            request.user.company.save()
    return redirect('settings')

@login_required
def leave_company(request):
    if request.user.company.owner == request.user:
        request.user.company.delete()
    request.user.company = None
    request.user.role = None
    request.user.save()
    return redirect('settings')

@login_required
def add_role(request):
    if request.user.role.manage_roles_access:
        if request.method.lower() == 'post':
            role = Role.objects.create(
                company=request.user.company,
                name=request.POST.get('name'),
                user_info_access=CHECKBOX_MAPPING[request.POST.get('user_info_access')],
                detailed_project_info_access=CHECKBOX_MAPPING[request.POST.get('detailed_project_info_access')],
                project_manage_access=CHECKBOX_MAPPING[request.POST.get('project_manage_access')],
                invite_user_access=CHECKBOX_MAPPING[request.POST.get('invite_user_access')],
                kick_user_access=CHECKBOX_MAPPING[request.POST.get('kick_user_access')],
                expenses_manage_access=CHECKBOX_MAPPING[request.POST.get('expenses_manage_access')],
                invoices_manage_access=CHECKBOX_MAPPING[request.POST.get('invoices_manage_access')],
                client_manage_access=CHECKBOX_MAPPING[request.POST.get('client_manage_access')],
                task_manage_access=CHECKBOX_MAPPING[request.POST.get('task_manage_access')],
                expense_category_manage_access=CHECKBOX_MAPPING[request.POST.get('expense_category_manage_access')],
                edit_company_info_access=CHECKBOX_MAPPING[request.POST.get('edit_company_info_access')],
                manage_roles_access=CHECKBOX_MAPPING[request.POST.get('manage_roles_access')]
            )
            role.save()
    return redirect('settings')

@login_required
def edit_role(request, pk):
    if request.user.role.manage_roles_access:
        if request.method.lower() == 'post':
            role = get_object_or_404(Role, company=request.user.company, pk=pk)
            if role != request.user.company.owner.role:
                role.company = request.user.company
                role.name = request.POST.get('name')
                role.user_info_access = CHECKBOX_MAPPING[request.POST.get('user_info_access')]
                role.detailed_project_info_access = CHECKBOX_MAPPING[request.POST.get('detailed_project_info_access')]
                role.project_manage_access = CHECKBOX_MAPPING[request.POST.get('project_manage_access')]
                role.invite_user_access = CHECKBOX_MAPPING[request.POST.get('invite_user_access')]
                role.kick_user_access = CHECKBOX_MAPPING[request.POST.get('kick_user_access')]
                role.expenses_manage_access = CHECKBOX_MAPPING[request.POST.get('expenses_manage_access')]
                role.invoices_manage_access = CHECKBOX_MAPPING[request.POST.get('invoices_manage_access')]
                role.client_manage_access = CHECKBOX_MAPPING[request.POST.get('client_manage_access')]
                role.task_manage_access = CHECKBOX_MAPPING[request.POST.get('task_manage_access')]
                role.expense_category_manage_access = CHECKBOX_MAPPING[request.POST.get('expense_category_manage_access')]
                role.edit_company_info_access = CHECKBOX_MAPPING[request.POST.get('edit_company_info_access')]
                role.manage_roles_access = CHECKBOX_MAPPING[request.POST.get('manage_roles_access')]
                role.save()
    return redirect('settings')

@login_required
def delete_role(request, pk):
    if request.user.role.manage_roles_access:
        role = get_object_or_404(Role, company=request.user.company, pk=pk)
        role.delete()
    return redirect('settings')
