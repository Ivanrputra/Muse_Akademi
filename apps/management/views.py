from django.shortcuts import render
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from core.models import MentorData,Course
from core.decorators import user_required,mentor_required
# from . import forms

# Create your views here.\
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
    
