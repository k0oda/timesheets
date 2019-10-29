from django.shortcuts import render, redirect
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

    @staticmethod
    @login_required
    def edit_user(request):
        if request.method.lower() == 'post':
            request.user.username = request.POST.get('username')
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.save()
        return redirect('settings')
