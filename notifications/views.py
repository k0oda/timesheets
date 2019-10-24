from django.shortcuts import render
from notifications.models import Invitation
from django.contrib.auth.decorators import login_required
from company_panel.models import Company


class Notifications:
    @staticmethod
    @login_required
    def notifications(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = -1

        notifications = Invitation.objects.filter(target_user=request.user)
        return render(request, 'notifications/notifications.html', context={
            'company': company,
            'notifications': notifications
        })
