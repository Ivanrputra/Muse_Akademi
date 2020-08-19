from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView

from core.decorators import mentor_required,staff_required

from . import views

app_name = 'management'

urlpatterns = [
	path('dashboard/', 		staff_required(TemplateView.as_view(http_method_names=['get'],template_name="management/dashboard.html")),name='dashboard'),
	
	path('course/<int:pk>', views.CoursePreview.as_view(http_method_names=['get']),name='course-preview'),
	
	path('courses/', views.CourseCreate.as_view(http_method_names=['get','post']),name='courses'),
	path('course/update/<int:pk>', views.CourseUpdate.as_view(http_method_names=['get','post']),name='course-update'),
	path('course/delete/<int:pk>', views.CourseDelete.as_view(http_method_names=['post']),name='course-delete'),

	path('classroom/<int:pk>', views.ClassroomDashboard.as_view(http_method_names=['get']),name='classroom'),
	
	path('classroom/<int:course_pk>/exam', views.ExamCreate.as_view(http_method_names=['get','post']),name='exam'),
	path('classroom/exam/<int:pk>/update', views.ExamUpdate.as_view(http_method_names=['get','post']),name='exam-update'),
	path('classroom/exam/<int:pk>/delete', views.ExamDelete.as_view(http_method_names=['post']),name='exam-delete'),
	
	path('classroom/<int:course_pk>/session/create', views.SessionCreate.as_view(http_method_names=['get','post']),name='session-create'),
	path('classroom/session/<int:pk>/update', views.SessionUpdate.as_view(http_method_names=['get','post']),name='session-update'),
	path('classroom/session/<int:pk>/delete', views.SessionDelete.as_view(http_method_names=['post']),name='session-delete'),
	path('classroom/session/<int:pk>', views.ClassroomSession.as_view(http_method_names=['get']),name='classroom-session'),

	path('sessiondata/<int:session_pk>', views.SessionDataCreate.as_view(http_method_names=['post']),name='sessiondata'),
	path('sessiondata/delete/<int:pk>', views.SessionDataDelete.as_view(http_method_names=['post']),name='sessiondata-delete'),

	path('classroom/<int:pk>/students', views.CourseStudentsList.as_view(http_method_names=['get']),name='course-students'),
	path('classroom/report/<int:pk>', views.ExamReport.as_view(http_method_names=['get']),name='report'),
	
	path('mentor/', views.MentorManagement.as_view(http_method_names=['get']),name='mentor-management'),
	path('mentor/<int:pk>', views.MentorManagementUpdate.as_view(http_method_names=['get','post']),name='mentor-update'),

	path('order/', views.OrderManagement.as_view(http_method_names=['get']),name='order-management'),
	path('order/<int:pk>', views.OrderManagementUpdate.as_view(http_method_names=['get','post']),name='order-update'),
	
]
