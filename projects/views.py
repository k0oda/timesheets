from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from projects.models import Project
from manage_app.models import Client, Task
from times.models import Entry
from datetime import time, timedelta, datetime


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
    def project(request, pk):
        if request.user.role.detailed_project_info_access:
            project = Project.objects.get(company=request.user.company, pk=pk)
            team = get_user_model().objects.filter(company=request.user.company)
            totals = {}
            for user in team:
                entries = Entry.objects.filter(company=request.user.company, user=user, project=project)
                if entries:
                    totals[user.username] = time(0, 0)
                    for entry in entries:
                        timer_delta = timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)
                        current_total = totals[user.username]
                        totals[user.username] = (datetime.min + (timedelta(hours=current_total.hour, minutes=current_total.minute) + timer_delta)).time()
            return render(request, 'projects/project.html', context={
                'project': project,
                'totals': totals
            })
        else:
            return redirect('projects')

    @staticmethod
    @login_required
    def add_project(request):
        if request.user.role.project_manage_access:
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
        if request.user.role.project_manage_access:
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
        if request.user.role.project_manage_access:
            project = Project.objects.get(company=request.user.company, pk=pk)
            project.delete()
        return redirect('projects')
