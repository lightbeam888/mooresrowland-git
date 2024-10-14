from django import template
import pprint

register = template.Library()

@register.simple_tag
def debug_object(obj):
    return pprint.pformat({
        'str': str(obj),
        'dir': dir(obj)
    })