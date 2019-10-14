from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company


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
        return render(request, 'manage/clients.html', context={'company': company})
