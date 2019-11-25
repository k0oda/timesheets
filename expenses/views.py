from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
from projects.models import Project
from manage_app.models import Category


class Expenses:
    @staticmethod
    @login_required
    def expenses(request):
        expenses = Expense.objects.filter(company=request.user.company).order_by('-date')
        projects = Project.objects.filter(company=request.user.company)
        categories = Category.objects.filter(company=request.user.company)

        return render(request, 'expenses/expenses.html', context={
            'expenses': expenses,
            'projects': projects,
            'categories': categories
        })

    @staticmethod
    @login_required
    def add_expense(request):
        if request.method.lower() == 'post':
            project = Project.objects.get(name=request.POST.get('project'), company=request.user.company)
            category = Category.objects.get(name=request.POST.get('category'), company=request.user.company)
            notes = request.POST.get('notes')
            amount = request.POST.get('amount')
            
            expense = Expense.objects.create(
                company=request.user.company,
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
            expense = Expense.objects.get(pk=expense_id, company=request.user.company)
            project = Project.objects.get(name=request.POST.get('project'), company=request.user.company)
            category = Category.objects.get(name=request.POST.get('category'), company=request.user.company)
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
        expense = Expense.objects.get(pk=expense_id, company=request.user.company)
        expense.project.total_spent -= expense.amount
        expense.project.save()
        expense.delete()
        return redirect('expenses')
