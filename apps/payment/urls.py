from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from . import views

app_name = 'payment'

urlpatterns = [

    # LANDING PAGE
    path('notification_handler/', views.notification_handler.as_view(),name='index'),
    path('finish/', views.finish.as_view(),name='finish'),
    path('unfinish/', views.unfinish.as_view(),name='unfinish'),
    path('error/', views.error.as_view(),name='error'),
    # path('test/<int:pk>', views.TestView.as_view(),name='test'),
 
    
]
