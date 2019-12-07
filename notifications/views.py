from django.shortcuts import render
from notifications.models import Invitation
from django.contrib.auth.decorators import login_required

@login_required
def notifications(request):
    notifications = Invitation.objects.filter(target_user=request.user)

    return render(request, 'notifications/notifications.html', context={
        'notifications': notifications
    })
