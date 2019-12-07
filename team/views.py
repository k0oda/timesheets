from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from notifications.models import Invitation
from times.models import Entry
from company_panel.models import Role

@login_required
def team(request):
    team = get_user_model().objects.filter(company=request.user.company)

    return render(request, 'team/team.html', context={
        'team': team
    })

@login_required
def invite(request):
    if request.user.role.invite_user_access:
        if request.method.lower() == 'post':
            user = get_object_or_404(get_user_model(), username=request.POST.get('username'))
            new_invitation = Invitation.objects.create(
                company = request.user.company,
                target_user = user
            )
            new_invitation.save()
    return redirect('team')

@login_required
def accept_invitation(request, pk):
    invitation = get_object_or_404(Invitation, pk=pk)
    request.user.company = invitation.company
    request.user.save()
    invitation.delete()
    return redirect('time')

@login_required
def user_profile(request, pk):
    if request.user.role.user_info_access:
        user = get_object_or_404(get_user_model(), company=request.user.company, pk=pk)
        entries = Entry.objects.filter(user=user)
        roles = Role.objects.filter(company=request.user.company)

        return render(request, 'team/user_profile.html', context={
            'user': user,
            'entries': entries,
            'roles': roles
        })
    else:
        return redirect('team')

@login_required
def edit_user_role(request, pk):
    if request.user.role.manage_roles_access:
        if request.method.lower() == 'post':
            user = get_object_or_404(get_user_model(), company=request.user.company, pk=pk)
            user.role = get_object_or_404(Role, name=request.POST.get('role'), company=request.user.company)
            user.save()
    return redirect('user_profile', pk)

@login_required
def kick_user(request, pk):
    if request.user.role.kick_user_access:
        user_to_kick = get_object_or_404(get_user_model(), company=request.user.company, pk=pk)

        if request.user == request.user.company.owner and request.user != user_to_kick:
            user_to_kick.company_id = None
            user_to_kick.save()
    return redirect('team')
