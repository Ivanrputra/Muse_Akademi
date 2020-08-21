from django.utils.safestring import mark_safe
from django.template import Library
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

import json,os

register = Library()

def pic_helper(obj,url):
    if not obj : return url
    if not os.path.exists(obj.path): return url
    return obj.url

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter(is_safe=True)
def profile_pic(obj):
    return pic_helper(obj,'/static/img/blank-avatar.png')

@register.filter(is_safe=True)
def course_pic(obj):
    return pic_helper(obj,'/static/img/blank-course.png')

@register.filter(is_safe=True)
def category_pic(obj):
    return pic_helper(obj,'/static/img/blank-category.png')

@register.filter(is_safe=True)
def order_pic(obj):
    return pic_helper(obj,'#')

@register.filter(is_safe=True)
def mentor_data(obj):
    if not obj : return '#'
    return obj.url

@register.filter(is_safe=True)
def is_active_now(obj):
    if obj < timezone.now():
        return 'success'
    return 'warning'

@register.filter
def publish_is(queryset, is_publish):
    return queryset.filter(is_publish=is_publish)

@register.filter
def list_status(queryset, status):
    if status == 'active':
        return queryset.filter(start_at__lte=timezone.now().date(),close_at__gte=timezone.now().date()).distinct()
    elif status == 'new':
        return queryset.filter(start_at__gt=timezone.now().date()).distinct()
    elif status == 'not active':
        return queryset.filter(Q(close_at__gt=timezone.now().date())|Q(start_at__lt=timezone.now().date())).distinct()
    elif status == 'done':
        return queryset.filter(close_at__lt=timezone.now().date()).distinct()    

@register.filter
def session_status(queryset, status):
    if status == "active":
        return queryset.filter(start_at__gte=timezone.now().date()).distinct()
    elif status == "not active":
        return queryset.filter(start_at__lt=timezone.now().date()).distinct()

@register.filter
def filter_mentor_status(queryset, status):
    if status == 'accepted':
        return queryset.filter(status='AC')
    elif status == 'waiting':
        return queryset.filter(status='WA')
    elif status == 'decline':
        return queryset.filter(status='DE')

@register.filter
def filter_order_status(queryset, status):
    if status == 'waiting payment':
        return queryset.filter(status='WP')
    elif status == 'waiting confirmation':
        return queryset.filter(status='WC')
    elif status == 'confirmed':
        return queryset.filter(status='CO')
    elif status == 'decline':
        return queryset.filter(status='DE')