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
    path('dashboard/', views.Dashboard.as_view(),name='dashboard'),

# CERTIFICATE
    # path('pdf/<int:classroom_pk>', views.CertificatePDFView.as_view(),name='certificate'),

# SERVE PROTECTED MEDIA
    # path('download/course_file/<int:tutor_id>/<int:course_id>/<str:media>/<str:path>',views.serve_protected,name="serve-protected"),

# CUSTOM ERROR PAGE
    # path('404', views.page_not_found),
    # path('403', views.page_permission_denied),
]
