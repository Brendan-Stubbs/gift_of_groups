from django import template
# from django.template.loader import render_to_string
from django.urls import reverse
from gift_of_groups.local_settings import DOMAIN_NAME

register = template.Library()

@register.simple_tag(takes_context=True)
def abs_url(context, view_name, *args, **kwargs):
    try:
        return context['request'].build_absolute_uri(
            reverse(view_name, args=args, kwargs=kwargs)
        )
    except KeyError:
        return DOMAIN_NAME
