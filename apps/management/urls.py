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
	path('courses/', 		staff_required(TemplateView.as_view(template_name="management/courses.html")),	name='courses'),
	
	path('course/<int:pk>', views.CourseDetail.as_view(),name='course'),
	path('mentor/<int:pk>', views.MentorManagement.as_view(),name='mentor-management'),
	
]
