from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from projects.models import Project
from manage_app.models import Client, Task


class Projects:
    @staticmethod
    @login_required
    def projects(request):
        projects = Project.objects.filter(company=request.user.company)
        clients = Client.objects.filter(company=request.user.company)
        tasks = Task.objects.filter(company=request.user.company)
        return render(request, 'projects/projects.html', context={
            'projects': projects,
            'clients': clients,
            'tasks': tasks
        })

    @staticmethod
    @login_required
    def add_project(request):
        if request.method.lower() == 'post':
            name = request.POST.get('name')
            client = Client.objects.get(company=request.user.company, name=request.POST.get('client'))
            notes = request.POST.get('notes')
            budget = request.POST.get('budget')
            new_project = Project.objects.create(
                company=request.user.company,
                name=name,
                client=client,
                notes=notes,
                budget=budget
            )
            tasks = request.POST.getlist('tasks')
            for task in tasks:
                new_project.tasks.add(Task.objects.get(company=request.user.company, name=task))
            new_project.save()
        return redirect('projects')

    @staticmethod
    @login_required
    def edit_project(request, pk):
        if request.method.lower() == 'post':
            project = Project.objects.get(company=request.user.company, pk=pk)
            project.name = request.POST.get('name')
            project.client = Client.objects.get(company=request.user.company, name=request.POST.get('client'))
            project.notes = request.POST.get('notes')
            project.budget = request.POST.get('budget')
            project.tasks.clear()
            tasks = request.POST.getlist('tasks')
            for task in tasks:
                project.tasks.add(Task.objects.get(company=request.user.company, name=task))
            project.save()
        return redirect('projects')

    @staticmethod
    @login_required
    def delete_project(request, pk):
        project = Project.objects.get(company=request.user.company, pk=pk)
        project.delete()
        return redirect('projects')
