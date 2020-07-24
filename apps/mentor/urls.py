from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.views.generic import TemplateView

from core.decorators import mentor_required

from . import views

app_name = 'mentor'

urlpatterns = [
	path('register/', views.MentorRegister.as_view(),name='register'),

	path('dashboard/', views.Dashboard.as_view(),name='dashboard'),
	path('courses/',   mentor_required(TemplateView.as_view(template_name="mentor/courses.html")),name='courses'),
	path('schedule/',  mentor_required(TemplateView.as_view(template_name="mentor/schedule.html")),name='schedule'),
]
