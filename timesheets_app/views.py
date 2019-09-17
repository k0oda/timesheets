from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from timesheets_app.models import Company
from authentication.models import UserProfile
from timesheets_app.forms import CreateCompanyForm
from datetime import date


class Main:
    @staticmethod
    def main(request):
        if request.user.is_authenticated:
            company_id = UserProfile.objects.get(username=request.user.username).company_id
            if Company.objects.filter(pk=company_id).exists():
                company = Company.objects.get(pk=company_id)
            else:
                company = 0
            return render(request, 'timesheets/company_header.html', context={'company': company})
        else:
            return render(request, 'timesheets/unauthenticated.html')

    @staticmethod
    @login_required
    def new_company(request):
        if request.method.lower() == 'post':
            form = CreateCompanyForm(request.POST)
            company = form.save(commit=False)
            user = UserProfile.objects.get(username=request.user.username)
            company.save()
            user.company_id = company.pk
            user.save()
            return redirect('/')
        else:
            form = CreateCompanyForm()
        return render(request, 'timesheets/new_company.html', {'form': form})


class CompanyPanel:
    @staticmethod
    @login_required
    def time(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0

        today = date.today()
        weekday = today.strftime('%A')
        return render(request, 'timesheets/company_panel/time.html', context={'company': company, 'today': today, 'weekday': weekday})

    @staticmethod
    @login_required
    def expenses(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/expenses.html', context={'company': company})

    @staticmethod
    @login_required
    def projects(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/projects.html', context={'company': company})

    @staticmethod
    @login_required
    def team(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/team.html', context={'company': company})

    @staticmethod
    @login_required
    def invoices(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/invoices.html', context={'company': company})

    @staticmethod
    @login_required
    def manage(request):
        company_id = UserProfile.objects.get(username=request.user.username).company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/manage.html', context={'company': company})
