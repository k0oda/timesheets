from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.conf import settings
from notifications.models import Invitation
from times.models import Entry
from company_panel.models import Role
from .forms import InviteUser, EditUserRole, EditUserHourlyRate

@login_required
def team(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    pages = Paginator(get_user_model().objects.filter(company=request.user.company), settings.ITEMS_PER_PAGE)
    team = pages.page(page).object_list
    return render(request, 'team/team.html', context={
        'team': team,
        'pages': pages,
        'current_page': page,
    })

@login_required
def invite(request):
    if request.user.role.invite_user_access:
        if request.method.lower() == 'post':
            form = InviteUser(data=request.POST)
            if form.is_valid():
                user = get_object_or_404(get_user_model(), username=form.cleaned_data['username'])
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

        return render(request, 'team/user_profile.html', context={
            'user': user,
            'entries': entries
        })
    else:
        return redirect('team')

@login_required
def edit_user_role(request, pk):
    if request.user.role.manage_roles_access:
        if request.method.lower() == 'post':
            form = EditUserRole(request.user, data=request.POST)
            if form.is_valid():
                user = get_object_or_404(get_user_model(), company=request.user.company, pk=pk)
                user.role = form.cleaned_data['role']
                user.save()
    return redirect('user_profile', pk)

@login_required
def edit_user_hourly_rate(request, pk):
    if request.user.role.manage_hourly_rates_access:
        if request.method.lower() == 'post':
            form = EditUserHourlyRate(request.user, data=request.POST)
            if form.is_valid():
                user = get_object_or_404(get_user_model(), company=request.user.company, pk=pk)
                print("abcd")
                print(form.cleaned_data['hourly_rate'])
                user.hourly_rate = form.cleaned_data['hourly_rate']
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
