from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company, Role
from company_panel.forms import CreateCompanyForm


class CompanyPanel:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            return redirect('time')
        else:
            return render(request, 'company_panel/unauthenticated.html')

    @staticmethod
    @login_required
    def new_company(request):
        if request.method.lower() == 'post':
            form = CreateCompanyForm(request.POST)
            company = form.save(commit=False)
            user = request.user
            company.owner = user
            company.save()
            user.company_id = company.pk
            user.save()
            return redirect('/')
        else:
            form = CreateCompanyForm()
        return render(request, 'company_panel/new_company.html', {'form': form})
    
    @staticmethod
    @login_required
    def add_role(request):
        if request.user.role.manage_roles_access:
            if request.method.lower() == 'post':
                role = Role.objects.create(
                    company=request.user.company,
                    name=request.POST.get('name'),
                    user_info_access=request.POST.get('user_info_access'),
                    detailed_project_info_access=request.POST.get('detailed_project_info_access'),
                    project_manage_access=request.POST.get('project_manage_access'),
                    invite_user_access=request.POST.get('invite_user_access'),
                    kick_user_access=request.POST.get('kick_user_access'),
                    expenses_manage_access=request.POST.get('expenses_manage_access'),
                    invoices_manage_access=request.POST.get('invoices_manage_access'),
                    client_manage_access=request.POST.get('client_manage_access'),
                    task_manage_access=request.POST.get('task_manage_access'),
                    expense_category_manage_access=request.POST.get('expense_category_manage_access'),
                    edit_company_info_access=request.POST.get('edit_company_info_access'),
                    manage_roles_access=request.POST.get('manage_roles_access')
                )
                role.save()
        return redirect('settings')
