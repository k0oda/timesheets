from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from projects.models import Project
from manage_app.models import Client, Task
from times.models import Entry
from datetime import time, timedelta, datetime
from .forms import CreateProject

@login_required
def projects(request):
    projects = Project.objects.filter(company=request.user.company)
    return render(request, 'projects/projects.html', context={
        'projects': projects
    })

@login_required
def project(request, pk):
    if request.user.role.detailed_project_info_access:
        project = get_object_or_404(Project, company=request.user.company, pk=pk)
        entries = Entry.objects.filter(company=request.user.company, project=project).order_by('user__username')
        totals = {}
        last_username = None
        for entry in entries:
            if entry.user.username != last_username:
                totals[entry.user.username] = time(0, 0)
                last_username = entry.user.username
            timer_delta = timedelta(hours=entry.timer.hour, minutes=entry.timer.minute)
            current_total = totals[entry.user.username]
            totals[entry.user.username] = (datetime.min + (timedelta(hours=current_total.hour, minutes=current_total.minute) + timer_delta)).time()
        return render(request, 'projects/project.html', context={
            'project': project,
            'totals': totals
        })
    else:
        return redirect('projects')

@login_required
def add_project(request):
    if request.user.role.project_manage_access:
        if request.method.lower() == 'post':
            form = CreateProject(request.user, data=request.POST)
            new_project = form.save(commit=False)
            new_project.company = request.user.company
            new_project.save()
            form.save_m2m()
    return redirect('projects')

@login_required
def edit_project(request, pk):
    if request.user.role.project_manage_access:
        if request.method.lower() == 'post':
            project = get_object_or_404(Project, company=request.user.company, pk=pk)
            form = CreateProject(request.user, project, data=request.POST)
            new_project = form.save(commit=False)
            new_project.company = project.company
            new_project.save()
            form.save_m2m()
            project.name = new_project.name
            project.client = new_project.client
            project.notes = new_project.notes
            project.budget = new_project.budget
            project.tasks.set(new_project.tasks.all())
            new_project.delete()
            project.save()
    return redirect('projects')

@login_required
def delete_project(request, pk):
    if request.user.role.project_manage_access:
        project = get_object_or_404(Project, company=request.user.company, pk=pk)
        project.delete()
    return redirect('projects')
