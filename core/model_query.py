from django.utils import timezone
from .models import *

def get_active_course():
    return Course.objects.filter(is_publish=True,start_at__gt=timezone.now().date())

def get_all_course():
    return Course.objects.all()