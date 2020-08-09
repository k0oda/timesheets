from django.shortcuts import render
from notifications.models import Invitation
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings

@login_required
def notifications(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    pages = Paginator(Invitation.objects.filter(target_user=request.user), settings.ITEMS_PER_PAGE)
    notifications = pages.page(page).object_list

    return render(request, 'notifications/notifications.html', context={
        'notifications': notifications,
        'pages': pages,
        'current_page': page,
    })
