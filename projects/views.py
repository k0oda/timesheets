from django.shortcuts import render
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

