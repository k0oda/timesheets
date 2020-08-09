from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from expenses.models import Expense
from projects.models import Project
from manage_app.models import Category
from .forms import CreateExpense

@login_required
def expenses(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    projects = Project.objects.filter(company=request.user.company)
    categories = Category.objects.filter(company=request.user.company)
    pages = Paginator(Expense.objects.filter(company=request.user.company).order_by('-date'), settings.ITEMS_PER_PAGE)
    expenses = pages.page(page).object_list

    return render(request, 'expenses/expenses.html', context={
        'expenses': expenses,
        'pages': pages,
        'current_page': page,
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
            form = CreateExpense(request.user, expense, data=request.POST)
            new_expense = form.save(commit=False)
            expense.project = new_expense.project
            expense.category = new_expense.category
            expense.notes = new_expense.notes
            expense.amount = new_expense.amount
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
