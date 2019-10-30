from django import template

register = template.Library()

@register.filter()
def is_numeric(value):
    return isinstance(value, int)
