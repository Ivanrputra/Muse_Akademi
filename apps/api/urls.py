from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register(r'category', views.CategoryView, basename='category')


app_name = 'api'

urlpatterns = [
    # path('hello/',views.HelloApiView.as_view(),name='hello'),
    # path('category/',views.CategoryView.as_view(),name='category'),
    
    path('category/',views.CategoryView.as_view({'get': 'list'}),name='category'),
    path('category/<int:pk>',views.CategoryView.as_view({'get': 'retrieve'}),name='category'),
    
    # tt1
    path(r'v1/', include(router.urls)),
]

