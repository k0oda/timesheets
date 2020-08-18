from importlib import import_module
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_form(name: str, *args, **kwargs):
    if settings.FORMS[name]:
        form_path = settings.FORMS[name]
        package, _class = form_path.rsplit('.', 1)
        module = import_module(package)
        form = getattr(module, _class)
        return form(*args, **kwargs)
