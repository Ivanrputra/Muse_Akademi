from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound,QueryDict,StreamingHttpResponse,FileResponse,Http404
from django.db import transaction
from django.db.models import Q,Count,Case, CharField, Value, When,IntegerField,Sum,Avg
from django.db.models.functions import Now
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse,reverse_lazy
from django.views.static import serve
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from core.models import Course,Session

# Create your views here.

class IndexView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CourseDetail(DetailView):
    model           = Course
    template_name   = "app/course_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DashboardClassroom(DetailView):
    model           = Course
    template_name   = "app/dashboard_classroom"

class ClassroomSession(DetailView):
    model           = Session
    template_name   = "app/classroom_session"

def page_not_found(request,exception=None):
    return render(request, '404.html')

def page_permission_denied(request,exception=None):
    return render(request, '403.html')
