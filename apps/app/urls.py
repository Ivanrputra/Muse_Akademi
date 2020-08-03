from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from . import views
from django.urls import re_path

app_name = 'app'

handler404 = views.page_not_found
handler403 = views.page_permission_denied

urlpatterns = [

# LANDING PAGE
    # path('q', TemplateView.as_view(template_name='testing/question.html')),
    path('', views.IndexView.as_view(),name='index'),
    path('dashboard/',  login_required(TemplateView.as_view(template_name="app/dashboard.html")),name='dashboard'),
    path('library/',    login_required(TemplateView.as_view(template_name="app/library.html")),name='library'),
    path('order/',      login_required(TemplateView.as_view(template_name="app/order.html")),name='order'),
    
    path('checkout/<int:pk>', login_required(views.Checkout.as_view()),name='checkout'),

    path('course/<int:pk>', views.CourseDetail.as_view(),name='course'),
    path('courses/', views.CourseList.as_view(),name='courses'),

    path('classroom/<int:pk>', views.DashboardClassroom.as_view(),name='dashboard-classroom'),
    path('classroom/session/<int:pk>', views.ClassroomSession.as_view(),name='classroom-session'),
    path('classroom/exams/<int:pk>', views.ClassroomExams.as_view(),name='classroom-exams'),
    path('classroom/exam/<int:pk>', views.ClassroomExamDetail.as_view(),name='classroom-exam'),

    path('examanswer/<int:exam_pk>', views.ExamAnswerCreate.as_view(),name='examanswer'),
	path('examanswer/update/<int:pk>', views.ExamAnswerUpdate.as_view(),name='examanswer-update'),
    path('examproject/<int:exam_pk>', views.ExamProjectCreate.as_view(),name='examproject'),
	path('examproject/delete/<int:pk>', views.ExamProjectDelete.as_view(),name='examproject-delete'),

    

# CERTIFICATE
    # path('pdf/<int:classroom_pk>', views.CertificatePDFView.as_view(),name='certificate'),

# SERVE PROTECTED MEDIA
    # path('download/course_file/<int:tutor_id>/<int:course_id>/<str:media>/<str:path>',views.serve_protected,name="serve-protected"),
    # path('download/<int:tutor_id>/<str:data>/<str:path>',views.serve_mentor_data),
    # path('pro/<int:tutor_id>/<str:data>/<str:path>',views.serve_mentor_data),

# CUSTOM ERROR PAGE
    # path('404', views.page_not_found),
    # path('403', views.page_permission_denied),
]
