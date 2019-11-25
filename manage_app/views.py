from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from manage_app.models import Client, Task, Category


class Manage:
    @staticmethod
    @login_required
    def base(request):
        return redirect('clients')

    @staticmethod
    @login_required
    def clients(request):
        clients = Client.objects.filter(company=request.user.company)

        return render(request, 'manage/clients.html', context={
            'clients': clients
        })

    @staticmethod
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

    @staticmethod
    @login_required
    def edit_client(request, pk):
        if request.user.role.client_manage_access:
            if request.method.lower() == 'post':
                client = Client.objects.get(pk=pk)
                client.name = request.POST.get('name')
                client.email = request.POST.get('email')
                client.save()
        return redirect('clients')

    @staticmethod
    @login_required
    def delete_client(request, pk):
        if request.user.role.client_manage_access:
            client = Client.objects.get(pk=pk)
            client.delete()
        return redirect('clients')

    @staticmethod
    @login_required
    def tasks(request):
        tasks = Task.objects.filter(company=request.user.company)

        return render(request, 'manage/tasks.html', context={
            'tasks': tasks
        })

    @staticmethod
    @login_required
    def add_task(request):
        if request.user.role.task_manage_access:
            if request.method.lower() == 'post':
                name = request.POST.get('name')
                hourly_rate = request.POST.get('hourly_rate')
                new_task = Task.objects.create(
                    company=request.user.company,
                    name=name,
                    default_hourly_rate=hourly_rate
                )
                new_task.save()
        return redirect('tasks')

    @staticmethod
    @login_required
    def edit_task(request, pk):
        if request.user.role.task_manage_access:
            if request.method.lower() == 'post':
                task = Task.objects.get(pk=pk)
                task.name = request.POST.get('name')
                task.default_hourly_rate = request.POST.get('hourly_rate')
                task.save()
        return redirect('tasks')

    @staticmethod
    @login_required
    def delete_task(request, pk):
        if request.user.role.task_manage_access:
            task = Task.objects.get(pk=pk)
            task.delete()
        return redirect('tasks')

    @staticmethod
    @login_required
    def expense_categories(request):
        categories = Category.objects.filter(company=request.user.company)

        return render(request, 'manage/expense_categories.html', context={
            'categories': categories
        })

    @staticmethod
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

    @staticmethod
    @login_required
    def edit_category(request, pk):
        if request.user.role.expense_category_manage_access:
            if request.method.lower() == 'post':
                category = Category.objects.get(pk=pk)
                category.name = request.POST.get('name')
                category.save()
        return redirect('expense_categories')

    @staticmethod
    @login_required
    def delete_category(request, pk):
        if request.user.role.expense_category_manage_access:
            category = Category.objects.get(pk=pk)
            category.delete()
        return redirect('expense_categories')
