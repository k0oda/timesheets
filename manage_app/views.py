from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from manage_app.models import Client, Task, Category


class Manage:
    @staticmethod
    @login_required
    def base(request):
        return redirect('clients')

    @staticmethod
    @login_required
    def clients(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        clients = Client.objects.filter(company=company)

        return render(request, 'manage/clients.html', context={
            'company': company,
            'clients': clients
        })

    @staticmethod
    @login_required
    def add_client(request):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            name = request.POST.get('name')
            email = request.POST.get('email')
            new_client = Client.objects.create(
                company=company,
                name=name,
                email=email
            )
            new_client.save()
        return redirect('clients')

    @staticmethod
    @login_required
    def edit_client(request, pk):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            client = Client.objects.get(pk=pk)
            client.name = request.POST.get('name')
            client.email = request.POST.get('email')
            client.save()
        return redirect('clients')

    @staticmethod
    @login_required
    def delete_client(request, pk):
        company = Company.objects.get(pk=request.user.company_id)
        client = Client.objects.get(pk=pk)
        client.delete()
        return redirect('clients')

    @staticmethod
    @login_required
    def tasks(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        tasks = Task.objects.filter(company=company)

        return render(request, 'manage/tasks.html', context={
            'company': company,
            'tasks': tasks
        })

    @staticmethod
    @login_required
    def add_task(request):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            name = request.POST.get('name')
            hourly_rate = request.POST.get('hourly_rate')
            new_task = Task.objects.create(
                company=company,
                name=name,
                default_hourly_rate=hourly_rate
            )
            new_task.save()
        return redirect('tasks')

    @staticmethod
    @login_required
    def edit_task(request, pk):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            task = Task.objects.get(pk=pk)
            task.name = request.POST.get('name')
            task.default_hourly_rate = request.POST.get('hourly_rate')
            task.save()
        return redirect('tasks')

    @staticmethod
    @login_required
    def delete_task(request, pk):
        company = Company.objects.get(pk=request.user.company_id)
        task = Task.objects.get(pk=pk)
        task.delete()
        return redirect('tasks')

    @staticmethod
    @login_required
    def expense_categories(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        categories = Category.objects.filter(company=company)

        return render(request, 'manage/expense_categories.html', context={
            'company': company,
            'categories': categories
        })

    @staticmethod
    @login_required
    def add_category(request):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            name = request.POST.get('name')
            new_category = Category.objects.create(
                company=company,
                name=name
            )
            new_category.save()
        return redirect('expense_categories')

    @staticmethod
    @login_required
    def edit_category(request, pk):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            category = Category.objects.get(pk=pk)
            category.name = request.POST.get('name')
            category.save()
        return redirect('expense_categories')

    @staticmethod
    @login_required
    def delete_category(request, pk):
        company = Company.objects.get(pk=request.user.company_id)
        category = Category.objects.get(pk=pk)
        category.delete()
        return redirect('expense_categories')
