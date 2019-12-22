from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
from projects.models import Project
from manage_app.models import Category
from .forms import CreateExpense

@login_required
def expenses(request):
    expenses = Expense.objects.filter(company=request.user.company).order_by('-date')
    projects = Project.objects.filter(company=request.user.company)
    categories = Category.objects.filter(company=request.user.company)

    return render(request, 'expenses/expenses.html', context={
        'expenses': expenses,
        'form': CreateExpense(request.user)
    })

@login_required
def add_expense(request):
    if request.user.role.expenses_manage_access:
        if request.method.lower() == 'post':
            form = CreateExpense(request.user, data=request.POST)
            expense = form.save(commit=False)
            expense.company = request.user.company
            expense.save()
            project = expense.project
            project.total_spent += expense.amount
            project.save()
    return redirect('expenses')

@login_required
def edit_expense(request, expense_id):
    if request.user.role.expenses_manage_access:
        if request.method.lower() == 'post':
            expense = get_object_or_404(Expense, pk=expense_id, company=request.user.company)
            project = get_object_or_404(Project, name=request.POST.get('project'), company=request.user.company)
            category = get_object_or_404(Category, name=request.POST.get('category'), company=request.user.company)
            notes = request.POST.get('notes')
            amount = request.POST.get('amount')

            expense.project = project
            expense.category = category
            expense.notes = notes
            expense.amount = amount
            expense.save()
    return redirect('expenses')

@login_required
def delete_expense(request, expense_id):
    if request.user.role.expenses_manage_access:
        expense = get_object_or_404(Expense, pk=expense_id, company=request.user.company)
        expense.project.total_spent -= expense.amount
        expense.project.save()
        expense.delete()
    return redirect('expenses')
