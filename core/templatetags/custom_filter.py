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

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg

@register.filter(is_safe=True)
def is_active_now(obj):
    if obj < timezone.now(): return 'success'
    return 'warning'

@register.filter
def publish_is(queryset, is_publish):
    return queryset.filter(is_publish=is_publish)

@register.filter
def get_badge_mentor_status(status):
    if status      == 'WA' : return 'warning'
    elif status    == 'AC' : return 'success'
    elif status    == 'DE' : return 'danger'
    return 'warning'

@register.filter
def list_status(queryset, status):
    if status == 'active':
        queryset = queryset.filter(start_at__lte=timezone.now().date(),close_at__gte=timezone.now().date()).distinct()
    elif status == 'new':
        queryset = queryset.filter(start_at__gt=timezone.now().date()).distinct()
    elif status == 'not active':
        queryset = queryset.filter(Q(close_at__gt=timezone.now().date())|Q(start_at__lt=timezone.now().date())).distinct()
    elif status == 'done':
        queryset = queryset.filter(close_at__lt=timezone.now().date()).distinct()    
    return queryset

@register.filter
def count_query(queryset):
    return queryset.count()

@register.filter
def filter_mentordata_status(queryset,status):
    if status == "active":
        queryset = queryset.exclude(mentor__is_mentor=False)
    elif status == "not active":
        queryset = queryset.filter(mentor__is_mentor=False)
    return queryset

@register.filter
def session_status(queryset, status):
    if status == "active":
        queryset = queryset.filter(start_at__gte=timezone.now().date()).distinct()
    elif status == "not active":
        queryset = queryset.filter(start_at__lt=timezone.now().date()).distinct()
    return queryset

@register.filter
def filter_mentor_status(queryset, status):
    if status   == 'accepted':  queryset = queryset.filter(status='AC')
    elif status == 'waiting':   queryset = queryset.filter(status='WA')
    elif status == 'decline':   queryset = queryset.filter(status='DE')
    return queryset

@register.filter
def filter_order_status(queryset, status):
    if status == 'WP': 
        queryset = queryset.filter(status='WP')
    elif status == 'WC':  
        queryset = queryset.filter(status='WC')
    elif status == 'CO': 
        queryset = queryset.filter(status='CO')
    elif status == 'DE':   
        queryset = queryset.filter(status='DE')
    return queryset

@register.filter
def get_badge_order_status(status):
    if status      in ['WA','WC']   : return 'warning'
    elif status    == 'CO'          : return 'success'
    elif status    == 'DE'          : return 'danger'
    return 'warning'