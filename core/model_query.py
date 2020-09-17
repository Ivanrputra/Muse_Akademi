from django.utils import timezone
from .models import *
from django.db.models import Q

def get_active_course():
    return Course.objects.filter(is_publish=True,start_at__gte=timezone.now().date())

def get_active_free_course():
    return Course.objects.filter(Q(price=0)|Q(discount=100),is_publish=True,start_at__gte=timezone.now().date())

def get_all_course():
    return Course.objects.all()