from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# router.register(r'category', views.CategoryView, basename='category')
router.register(r'mentor/schedule', views.MentorScheduleView, basename='mentor-schedule')
router.register(r'course', views.CourseView, basename='course')

app_name = 'api'

urlpatterns = [
    # path('hello/',views.HelloApiView.as_view(),name='hello'),
    # path('category/',views.CategoryView.as_view(),name='category'),
    
    # CATEGORY
    path('category/',views.CategoryView.as_view({'get': 'list'}),name='category'),
    path('category/<int:pk>',views.CategoryView.as_view({'get': 'retrieve'}),name='category'),
    
    # path('course/',views.CourseView.as_view({'get': 'list'}),name='course'),

    path('course/user/',views.UserCourseView.as_view({'get': 'list'}),name='user-course'),
    path('order/user/',views.UserOrderView.as_view({'get': 'list'}),name='user-order'),

    # path('mentor/schedule/',views.MentorScheduleView.as_view({'get': 'list'}),name='user-order'),

    # tt1
    path(r'', include(router.urls)),
]

