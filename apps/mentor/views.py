from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound,QueryDict,StreamingHttpResponse,FileResponse,Http404
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,
                                DeleteView,FormView)
from django.views.generic.edit import FormMixin,ModelFormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.urls import reverse,reverse_lazy
from django.contrib import messages

from core.models import MentorData
from core.decorators import user_required,mentor_required
from . import forms

# Create your views here.\
# @method_decorator([user_required], name='dispatch')
class MentorRegister(CreateView):
    model           = MentorData
    template_name   = 'mentor/registration.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('mentor:register')

    def form_valid(self, form):
        form.instance.mentor = self.request.user
        return super().form_valid(form)

@method_decorator([user_required], name='dispatch')
class MentorRegisterUpdate(UpdateView):
    model           = MentorData
    template_name   = 'mentor/registration.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('mentor:register')

    def dispatch(self, request, *args, **kwargs):
        mentor_data = get_object_or_404(self.model,pk=self.kwargs.get(self.pk_url_kwarg),mentor=self.request.user)
        if mentor_data.status == 'AC':
            messages.success(self.request,'Anda sudah menjadi mentor')
            return HttpResponseRedirect(reverse_lazy('mentor:register'))
        return super().dispatch(request, *args, **kwargs)
