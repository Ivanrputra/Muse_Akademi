from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django.http import FileResponse,HttpResponseRedirect,Http404
from django.conf import settings
from django.urls import reverse,reverse_lazy
import os

from . import views
from django.urls import re_path

app_name = 'app'

handler404 = views.page_not_found
handler403 = views.page_permission_denied

def serve_protected(request,path_name,path_id,path):
    have_access = False
    if request.user.is_staff:
        have_access = True
    else:
        if path_name in ['mentor_data','order_attachment']:
            # path_id = user_id
            if request.user.id == path_id:
                have_access = True
        elif path_name in ['session_attachment']:
            # path_id = course_id
            lib = Library.objects.filter(user=request.user.id,course=path_id).exists()
            if lib : have_access = True
             
    if have_access:
        fullpath = os.path.join(settings.BASE_DIR,f'protected_media\{path_name}\{path_id}\{path}')
        try:
            return FileResponse(open(fullpath, 'rb'),as_attachment=True,filename=path)
        except :
            raise Http404
    else:
        return HttpResponseRedirect(reverse_lazy('app:index'))

urlpatterns = [

# LANDING PAGE
    # path('q', TemplateView.as_view(template_name='testing/question.html')),
    path('', views.IndexView.as_view(http_method_names=['get']),name='index'),
    path('courses', views.CourseList.as_view(http_method_names=['get']),name='courses'),
    path('course/<int:pk>', views.CourseDetail.as_view(http_method_names=['get']),name='course'),

    path('dashboard/',  login_required(TemplateView.as_view(http_method_names=['get'],template_name="app/dashboard.html")),name='dashboard'),
    path('library/',    login_required(TemplateView.as_view(http_method_names=['get'],template_name="app/library.html")),name='library'),
    path('order/',      login_required(TemplateView.as_view(http_method_names=['get'],template_name="app/order.html")),name='order'),
    path('order/<int:pk>',views.OrderDetailUpdate.as_view(http_method_names=['get','post']),name='order-detail'),

    path('checkout/<int:pk>', views.Checkout.as_view(http_method_names=['get']),name='checkout'),

    path('classroom/redirect/<int:pk>', views.ClassroomRedirectView.as_view(http_method_names=['get']), name='classroom-redirect'),

    path('classroom/library/<int:pk>', views.DashboardClassroom.as_view(http_method_names=['get']),name='dashboard-classroom'),
    path('classroom/session/<int:pk>', views.ClassroomSession.as_view(http_method_names=['get']),name='classroom-session'),
    path('classroom/<int:course_pk>/exams', views.ClassroomExams.as_view(http_method_names=['get']),name='classroom-exams'),

    path('examanswer/<int:exam_pk>', views.ExamAnswerCreate.as_view(http_method_names=['get','post']),name='examanswer'),
	path('examanswer/update/<int:pk>', views.ExamAnswerUpdate.as_view(http_method_names=['get','post']),name='examanswer-update'),
    path('examproject/<int:exam_pk>', views.ExamProjectCreate.as_view(http_method_names= ['post']),name='examproject'),
	path('examproject/delete/<int:pk>', views.ExamProjectDelete.as_view(http_method_names=['post']),name='examproject-delete'),

# CERTIFICATE
    path('certificate/<int:library_pk>', views.CertificatePDFView.as_view(http_method_names=['get']),name='certificate'),

# SERVE PROTECTED MEDIA
    # path('download/course_file/<int:tutor_id>/<int:course_id>/<str:media>/<str:path>',views.serve_protected,name="serve-protected"),
    # path('download/<int:tutor_id>/<str:data>/<str:path>',views.serve_mentor_data),
    # path('pro/<int:tutor_id>/<str:data>/<str:path>',views.serve_mentor_data),

    # SERVE PROTECTED MEDIA
    path('protected_media/<str:path_name>/<int:path_id>/<str:path>',serve_protected,name="serve-protected"),


# CUSTOM ERROR PAGE
    path('404', views.page_not_found),
    path('403', views.page_permission_denied),
]

