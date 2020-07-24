from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter

from . import views

# tt1
# router = DefaultRouter()
# router.register(r'message', MessageModelViewSet, basename='message-api')


app_name = 'api'

urlpatterns = [
    # path('hello/',views.HelloApiView.as_view(),name='hello'),
    path('category/',views.Category.as_view(),name='category'),
    
    # tt1
    # path(r'v1/', include(router.urls)),
]

