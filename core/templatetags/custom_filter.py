from django.utils.safestring import mark_safe
from django.template import Library

import json

register = Library()

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter(is_safe=True)
def profile_pic(obj):
    if not obj :
        return '/static/img/blank-avatar.png'
    return obj.url

@register.filter(is_safe=True)
def course_pic(obj):
    if not obj :
        return '/static/img/blank-course.png'
    return obj.url

@register.filter(is_safe=True)
def mentor_data(obj):
    if not obj :
        return '#'
    return obj.url

@register.filter(is_safe=True)
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    # value = unicode(value)

    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split(' ')[:-1]

    # Join the words and return
    return ' '.join(words) + '...'