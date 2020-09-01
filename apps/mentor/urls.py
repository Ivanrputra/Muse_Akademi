from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView

from core.decorators import mentor_required

from . import views

app_name = 'mentor'

urlpatterns = [
	path('profile/<int:pk>', views.MentorPublicProfile.as_view(http_method_names=['get']),name='profile'),
	path('profile/update', views.MentorPublicProfileUpdate.as_view(http_method_names=['get','post']),name='profile-update'),

	path('register/', views.MentorRegister.as_view(http_method_names=['get','post']),name='register'),
	path('register/update/<int:pk>', views.MentorRegisterUpdate.as_view(http_method_names=['get','post']),name='register-update'),

	path('dashboard/', mentor_required(TemplateView.as_view(http_method_names=['get'],template_name="mentor/dashboard.html")),name='dashboard'),
	path('courses/',   views.MentorCourses.as_view(http_method_names=['get']),name='courses'),
	path('schedule/',  mentor_required(TemplateView.as_view(http_method_names=['get'],template_name="mentor/schedule.html")),name='schedule'),

	path('classroom/<int:pk>', views.MentorClassroom.as_view(http_method_names=['get']),name='classroom'),
	path('classroom/session/<int:pk>', views.ClassroomSession.as_view(http_method_names=['get']),name='classroom-session'),
	path('classroom/<int:pk>/exams', views.ClassroomExams.as_view(http_method_names=['get']),name='classroom-exam'),

	path('classroom/<int:pk>/students', views.CourseStudentsList.as_view(http_method_names=['get']),name='course-students'),
	path('classroom/report/<int:examanswer_pk>', views.ExamReportCreate.as_view(http_method_names=['get','post']),name='report'),
	path('report/update/<int:pk>', views.ExamReportUpdate.as_view(http_method_names=['get','post']),name='report-update'),
]
