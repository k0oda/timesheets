from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from company_panel.models import Company
from authentication.models import UserProfile
from notifications.models import Invitation


class Team:
    @staticmethod
    @login_required
    def team(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        team = UserProfile.objects.filter(company=company)

        return render(request, 'team/team.html', context={
            'company': company,
            'team': team
        })

    @staticmethod
    @login_required
    def invite(request):
        if request.method.lower() == 'post':
            company = Company.objects.get(pk=request.user.company_id)
            user = UserProfile.objects.get(username=request.POST.get('username'))
            new_invitation = Invitation.objects.create(
                company = company,
                target_user = user
            )
            new_invitation.save()
        return redirect('team')

    @staticmethod
    @login_required
    def accept_invitation(request, pk):
        invitation = Invitation.objects.get(pk=pk)
        request.user.company_id = invitation.company.pk
        request.user.save()
        invitation.delete()
        return redirect('time')
