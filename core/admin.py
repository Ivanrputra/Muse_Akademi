from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models

class UserAdmin(admin.ModelAdmin):
	ordering		= ['id']
	list_display	= ['email','created_at']
	readonly_fields = ('created_at', )

	fieldsets		= (
		(None,{'fields':('email','username')}),
		(_('Personal Info'),{'fields':('firstname','lastname')}),
		(_('Permissions'),
			{'fields':('is_active','is_staff','is_superuser')}
		),
		(_('Important dates'),{'fields':('last_login',)})
	)

admin.site.register(models.User,UserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Session)
admin.site.register(models.Library)

