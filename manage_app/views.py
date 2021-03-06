from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from manage_app.models import Client, Task
from manage_app.forms import CreateTask, CreateClient

@login_required
def manage(request):
    return redirect('clients')

@login_required
def clients(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    pages = Paginator(Client.objects.filter(company=request.user.company), settings.ITEMS_PER_PAGE)
    clients = pages.page(page).object_list

    return render(request, 'manage/clients.html', context={
        'clients': clients,
        'pages': pages,
        'current_page': page,
    })

@login_required
def add_client(request):
    if request.user.role.client_manage_access:
        if request.method.lower() == 'post':
            form = CreateClient(data=request.POST)
            new_client = form.save(commit=False)
            new_client.company = request.user.company
            new_client.save()
    return redirect('clients')

@login_required
def edit_client(request, pk):
    if request.user.role.client_manage_access:
        if request.method.lower() == 'post':
            client = get_object_or_404(Client, pk=pk)
            form = CreateClient(client, data=request.POST)
            new_client = form.save(commit=False)
            client.name = new_client.name
            client.email = new_client.email
            client.address = new_client.address
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
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    pages = Paginator(Task.objects.filter(company=request.user.company), settings.ITEMS_PER_PAGE)
    tasks = pages.page(page).object_list

    return render(request, 'manage/tasks.html', context={
        'tasks': tasks,
        'pages': pages,
        'current_page': page,
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
