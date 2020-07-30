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
	
	path('course/<int:pk>', views.CoursePreview.as_view(),name='course-preview'),
	
	path('courses/', views.CourseCreate.as_view(),name='courses'),
	path('course/update/<int:pk>', views.CourseUpdate.as_view(),name='course-update'),
	path('course/delete/<int:pk>', views.CourseDelete.as_view(),name='course-delete'),

	path('classroom/<int:course_pk>', views.SessionCreate.as_view(),name='classroom'),
	path('session/update/<int:pk>', views.SessionUpdate.as_view(),name='session-update'),
	path('session/delete/<int:pk>', views.SessionDelete.as_view(),name='session-delete'),

	path('sessiondata/<int:session_pk>', views.SessionDataCreate.as_view(),name='sessiondata'),
	path('sessiondata/delete/<int:pk>', views.SessionDataDelete.as_view(),name='sessiondata-delete'),

	path('exam/<int:course_pk>', views.ExamCreate.as_view(),name='exam'),
	path('exam/update/<int:pk>', views.ExamUpdate.as_view(),name='exam-update'),
	path('exam/delete/<int:pk>', views.ExamDelete.as_view(),name='exam-delete'),
	
	path('mentor/', views.MentorManagement.as_view(),name='mentor-management'),
	path('mentor/<int:pk>', views.MentorManagementUpdate.as_view(),name='mentor-update'),
	
]
