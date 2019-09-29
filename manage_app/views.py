from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from company_panel.models import Company


class Manage:
    @staticmethod
    @login_required
    def manage(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        return render(request, 'timesheets/company_panel/manage.html', context={'company': company})

