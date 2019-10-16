from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from manage_app.models import Client, Task


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
    def expense_categories(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'manage/expense_categories.html', context={'company': company})
