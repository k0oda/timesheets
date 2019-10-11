from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from projects.models import Project
from manage_app.models import Client, Task


class Projects:
    @staticmethod
    @login_required
    def projects(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        
        projects = Project.objects.filter(company=company)
        clients = Client.objects.filter(company=company)
        tasks = Task.objects.filter(company=company)
        return render(request, 'timesheets/company_panel/projects.html', context={
            'company': company,
            'projects': projects,
            'clients': clients,
            'tasks': tasks
        })

    @staticmethod
    @login_required
    def add_project(request):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            name = request.POST.get('name')
            client = Client.objects.get(company=company, name=request.POST.get('client'))
            notes = request.POST.get('notes')
            budget = request.POST.get('budget')
            new_project = Project.objects.create(
                company=company,
                name=name,
                client=client,
                notes=notes,
                budget=budget
            )
            tasks = request.POST.getlist('tasks')
            for task in tasks:
                new_project.tasks.add(Task.objects.get(company=company, name=task))
            new_project.save()
        return redirect('projects')

    @staticmethod
    @login_required
    def edit_project(request, pk):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            project = Project.objects.get(company=company, pk=pk)
            project.name = request.POST.get('name')
            project.client = Client.objects.get(company=company, name=request.POST.get('client'))
            project.notes = request.POST.get('notes')
            project.budget = request.POST.get('budget')
            project.tasks.clear()
            tasks = request.POST.getlist('tasks')
            for task in tasks:
                project.tasks.add(Task.objects.get(company=company, name=task))
            project.save()
        return redirect('projects')
