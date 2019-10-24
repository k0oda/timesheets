from django.shortcuts import render, redirect
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

        return render(request, 'expenses/expenses.html', context={
            'company': company,
            'expenses': expenses,
            'projects': projects,
            'categories': categories
        })

    @staticmethod
    @login_required
    def add_expense(request):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            project = Project.objects.get(name=request.POST.get('project'), company=company)
            category = Category.objects.get(name=request.POST.get('category'), company=company)
            notes = request.POST.get('notes')
            amount = request.POST.get('amount')
            
            expense = Expense.objects.create(
                company=company,
                project=project,
                category=category,
                notes=notes,
                amount=amount
            )
            expense.save()

            project.total_spent += float(amount)
            project.save()
        return redirect('expenses')

    @staticmethod
    @login_required
    def edit_expense(request, expense_id):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            expense = Expense.objects.get(pk=expense_id, company=company)
            project = Project.objects.get(name=request.POST.get('project'), company=company)
            category = Category.objects.get(name=request.POST.get('category'), company=company)
            notes = request.POST.get('notes')
            amount = request.POST.get('amount')

            expense.project = project
            expense.category = category
            expense.notes = notes
            expense.amount = amount
            expense.save()
        return redirect('expenses')

    @staticmethod
    @login_required
    def delete_expense(request, expense_id):
        company = Company.objects.get(pk=request.user.company_id)
        expense = Expense.objects.get(pk=expense_id, company=company)
        expense.delete()
        return redirect('expenses')
