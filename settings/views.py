from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from company_panel.models import Company


class Settings:
    @staticmethod
    @login_required
    def main(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = -1

        return render(request, 'settings/settings.html', context={
            'company': company
        })
