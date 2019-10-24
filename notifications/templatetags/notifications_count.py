from django import template
from notifications.models import Invitation

register = template.Library()

@register.simple_tag
def get_notifications_count(user):
    invitations = Invitation.objects.filter(target_user=user)
    return len(invitations)
