from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from expenses.models import Expense
from projects.models import Project
from manage_app.models import Category


class Expenses:
    @staticmethod
    @login_required
    def expenses(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0

        expenses = Expense.objects.filter(company=company).order_by('-date')
        projects = Project.objects.filter(company=company)
        categories = Category.objects.filter(company=company)

        return render(request, 'timesheets/company_panel/expenses.html', context={
            'company': company,
            'expenses': expenses,
            'projects': projects,
            'categories': categories
        })
