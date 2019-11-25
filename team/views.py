from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from notifications.models import Invitation
from times.models import Entry


class Team:
    @staticmethod
    @login_required
    def team(request):
        team = get_user_model().objects.filter(company=request.user.company)

        return render(request, 'team/team.html', context={
            'team': team
        })

    @staticmethod
    @login_required
    def invite(request):
        if request.user.role.invite_user_access:
            if request.method.lower() == 'post':
                user = get_user_model().objects.get(username=request.POST.get('username'))
                new_invitation = Invitation.objects.create(
                    company = request.user.company,
                    target_user = user
                )
                new_invitation.save()
        return redirect('team')

    @staticmethod
    @login_required
    def accept_invitation(request, pk):
        invitation = Invitation.objects.get(pk=pk)
        request.user.company = invitation.company
        request.user.save()
        invitation.delete()
        return redirect('time')

    @staticmethod
    @login_required
    def user_profile(request, pk):
        user = get_user_model().objects.get(company=request.user.company, pk=pk)
        entries = Entry.objects.filter(user=user)

        return render(request, 'team/user_profile.html', context={
            'user': user,
            'entries': entries
        })

    @staticmethod
    @login_required
    def kick_user(request, pk):
        user_to_kick = get_user_model().objects.get(company=request.user.company, pk=pk)

        if request.user == request.user.company.owner and request.user != user_to_kick:
            user_to_kick.company_id = None
            user_to_kick.save()
        return redirect('team')
