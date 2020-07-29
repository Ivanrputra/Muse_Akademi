from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView

from core.decorators import mentor_required,staff_required

from . import views

app_name = 'management'

urlpatterns = [
	path('dashboard/', 		staff_required(TemplateView.as_view(template_name="management/dashboard.html")),name='dashboard'),
	# path('courses/', 		staff_required(TemplateView.as_view(template_name="management/courses_list.html")),	name='courses'),

	path('courses/', views.CourseCreate.as_view(),name='courses'),
	path('course/<int:pk>', views.CourseDetail.as_view(),name='course'),
	path('course/update/<int:pk>', views.CourseUpdate.as_view(),name='course-update'),

	path('classroom/<int:course_pk>', views.SessionCreate.as_view(),name='classroom'),
	path('session/<int:pk>', views.SessionUpdate.as_view(),name='session-update'),

	# path('classroom/<int:pk>', views.ClassroomDetail.as_view(),name='classroom'),
	
	path('mentor/', views.MentorManagement.as_view(),name='mentor-management'),
	path('mentor/<int:pk>', views.MentorManagementUpdate.as_view(),name='mentor-update'),
	
]
