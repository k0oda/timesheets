from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from manage_app.models import Client, Task, Category
from manage_app.forms import CreateTask

@login_required
def manage(request):
    return redirect('clients')

@login_required
def clients(request):
    clients = Client.objects.filter(company=request.user.company)

    return render(request, 'manage/clients.html', context={
        'clients': clients
    })

@login_required
def add_client(request):
    if request.user.role.client_manage_access:
        if request.method.lower() == 'post':
            name = request.POST.get('name')
            email = request.POST.get('email')
            new_client = Client.objects.create(
                company=request.user.company,
                name=name,
                email=email
            )
            new_client.save()
    return redirect('clients')

@login_required
def edit_client(request, pk):
    if request.user.role.client_manage_access:
        if request.method.lower() == 'post':
            client = get_object_or_404(Client, pk=pk)
            client.name = request.POST.get('name')
            client.email = request.POST.get('email')
            client.save()
    return redirect('clients')

@login_required
def delete_client(request, pk):
    if request.user.role.client_manage_access:
        client = get_object_or_404(Client, pk=pk)
        client.delete()
    return redirect('clients')

@login_required
def tasks(request):
    tasks = Task.objects.filter(company=request.user.company)

    return render(request, 'manage/tasks.html', context={
        'tasks': tasks
    })

@login_required
def add_task(request):
    if request.user.role.task_manage_access:
        if request.method.lower() == 'post':
            form = CreateTask(data=request.POST)
            new_task = form.save(commit=False)
            new_task.company = request.user.company
            new_task.save()
    return redirect('tasks')

@login_required
def edit_task(request, pk):
    if request.user.role.task_manage_access:
        if request.method.lower() == 'post':
            task = get_object_or_404(Task, pk=pk)
            form = CreateTask(task, data=request.POST)
            new_task = form.save(commit=False)
            task.name = new_task.name
            task.default_hourly_rate = new_task.default_hourly_rate
            task.save()
    return redirect('tasks')

@login_required
def delete_task(request, pk):
    if request.user.role.task_manage_access:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    return redirect('tasks')

@login_required
def expense_categories(request):
    categories = Category.objects.filter(company=request.user.company)

    return render(request, 'manage/expense_categories.html', context={
        'categories': categories
    })

@login_required
def add_category(request):
    if request.user.role.expense_category_manage_access:
        if request.method.lower() == 'post':
            name = request.POST.get('name')
            new_category = Category.objects.create(
                company=request.user.company,
                name=name
            )
            new_category.save()
    return redirect('expense_categories')

@login_required
def edit_category(request, pk):
    if request.user.role.expense_category_manage_access:
        if request.method.lower() == 'post':
            category = get_object_or_404(Category, pk=pk)
            category.name = request.POST.get('name')
            category.save()
    return redirect('expense_categories')

@login_required
def delete_category(request, pk):
    if request.user.role.expense_category_manage_access:
        category = get_object_or_404(Category, pk=pk)
        category.delete()
    return redirect('expense_categories')
