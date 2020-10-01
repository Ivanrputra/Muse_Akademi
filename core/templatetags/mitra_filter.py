from django.utils.safestring import mark_safe
from django.template import Library
from django.core.files.storage import default_storage
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

import json,os

register = Library()

@register.filter
def admin_or_cohost(mitra, user):
    can_view = mitra.is_mitra_user_admin_or_cohost(user)
    return can_view