from django.shortcuts import render,get_object_or_404
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse,reverse_lazy

from core.models import MentorData,Course,Session
from core.decorators import user_required,mentor_required
from . import forms


# Create your views here.\

class CourseCreate(CreateView):
    model           = Course
    template_name   = 'management/courses.html'
    form_class      = forms.CourseForm
    success_url     = reverse_lazy('management:courses')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

class CourseUpdate(UpdateView):
    model           = Course
    template_name   = 'management/courses.html'
    form_class      = forms.CourseUpdateForm
    success_url     = reverse_lazy('management:courses')

# class ClassroomDetail(DetailView):
#     model           = Course
#     template_name   = 'management/classroom.html'

class SessionCreate(CreateView):
    model           = Session
    template_name   = 'management/classroom.html'
    form_class      = forms.SessionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        form.instance.course = course
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('mangement:classroom', kwargs={'course_pk':self.object.course.id})

class SessionUpdate(UpdateView):
    model           = Session
    template_name   = 'management/session_update.html'
    form_class      = forms.SessionForm
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'course_pk':self.object.course.id})

# @method_decorator([user_required], name='dispatch')
class CourseDetail(DetailView):
    model           = Course
    template_name   = 'management/course_detail.html'

class MentorManagement(TemplateView):
    template_name   = 'management/mentor_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor_accepted'] = MentorData.objects.filter(status='AC')
        context['mentor_waiting']  = MentorData.objects.filter(status='WA')
        context['mentor_decline']  = MentorData.objects.filter(status='DE')
        return context

class MentorManagementUpdate(UpdateView):
    model           = MentorData
    template_name   = 'management/mentor_management_update.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('management:mentor-management')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)
