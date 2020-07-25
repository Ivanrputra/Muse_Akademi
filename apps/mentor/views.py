from django.shortcuts import render
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator

from core.models import MentorData
from core.decorators import user_required,mentor_required
from . import forms

# Create your views here.\
@method_decorator([user_required], name='dispatch')
class MentorRegister(CreateView):
    model           = MentorData
    template_name   = 'mentor/registration.html'
    form_class      = forms.RegisterMentor
