from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from company_panel.forms import CreateCompanyForm


class CompanyPanel:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            company_id = request.user.company_id
            if Company.objects.filter(pk=company_id).exists():
                company = Company.objects.get(pk=company_id)
            else:
                company = 0
            return render(request, 'company_panel/company_header.html', context={'company': company})
        else:
            return render(request, 'company_panel/unauthenticated.html')

    @staticmethod
    @login_required
    def new_company(request):
        if request.method.lower() == 'post':
            form = CreateCompanyForm(request.POST)
            company = form.save(commit=False)
            user = request.user
            company.save()
            user.company_id = company.pk
            user.save()
            return redirect('/')
        else:
            form = CreateCompanyForm()
        return render(request, 'company_panel/new_company.html', {'form': form})
