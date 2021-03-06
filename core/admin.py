from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models

class UserAdmin(admin.ModelAdmin):
	ordering		= ['id']
	list_display	= ['email','created_at','is_active']
	readonly_fields = ('created_at', )

	fieldsets		= (
		(None,{'fields':('email','username','profile_pic')}),
		(_('Personal Info'),{'fields':('firstname','lastname')}),
		(_('Permissions'),
			{'fields':('is_active','is_mentor','is_staff','is_superuser')}
		),
		(_('Important dates'),{'fields':('last_login',)})
	)

admin.site.register(models.User,UserAdmin)
admin.site.register(models.MentorData)

admin.site.register(models.Category)
admin.site.register(models.Course)
admin.site.register(models.Session)
admin.site.register(models.SessionData)
admin.site.register(models.Mitra)
admin.site.register(models.MitraUser)
admin.site.register(models.MitraInvitedUser)

admin.site.register(models.Exam)
admin.site.register(models.ExamAnswer)
admin.site.register(models.ExamProject)
admin.site.register(models.ExamReport)
admin.site.register(models.Evaluation)
# admin.site.register(models.Quiz)
# admin.site.register(models.QuizChoice)

admin.site.register(models.Library)
# admin.site.register(models.CourseData)
admin.site.register(models.Order)
admin.site.register(models.Schedule)

admin.site.register(models.Institution)