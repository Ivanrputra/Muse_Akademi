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

from core.models import MentorData,Course,Library,ExamReport,ExamAnswer
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
    
    def dispatch(self, request, *args, **kwargs):
        mentor_data = self.model.objects.filter(mentor=self.request.user).first()
        if mentor_data:
            return HttpResponseRedirect(reverse_lazy('mentor:register-update',kwargs={'pk':mentor_data.id}))
        return super().dispatch(request, *args, **kwargs)

# @method_decorator([user_required], name='dispatch')
class MentorRegisterUpdate(UpdateView):
    model           = MentorData
    template_name   = 'mentor/registration.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('mentor:register')

    def form_valid(self, form):
        form.instance.status = 'WA'
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # mentor_data = get_object_or_404(self.model,pk=self.kwargs.get(self.pk_url_kwarg),mentor=self.request.user)
        # if mentor_data.status == 'AC':
        #     messages.success(self.request,'Anda sudah menjadi mentor')
        #     return HttpResponseRedirect(reverse_lazy('mentor:register'))
        return super().dispatch(request, *args, **kwargs)

class CourseStudentsList(DetailView):
    model               = Course
    template_name       = "mentor/course_students.html"
    context_object_name = "course"
    
class CourseStudentExam(DetailView):
    model               = ExamAnswer
    template_name       = "mentor/course_student_exam.html"
    context_object_name = "exam_answer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reportmentor']   = ExamReport.objects.filter(mentor=self.request.user,exam_answer=self.object).first()
        if context['reportmentor']:
            context['form'] = forms.ExamReportForm(instance=context['reportmentor'])
        else:
            context['form'] = forms.ExamReportForm
        return context
    
class ExamReportCreate(CreateView):
    model           = ExamReport
    form_class      = forms.ExamReportForm

    def form_valid(self, form):
        exam_answer = get_object_or_404(ExamAnswer,pk=self.kwargs['examanswer_pk'])
        ins = form.instance
        form.instance.exam_answer   = exam_answer
        form.instance.mentor        = self.request.user
        form.instance.summary       = (ins.ide + ins.konsep + ins.desain + ins.proses + ins.produk) / 5
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('mentor:student-exam', kwargs={'pk':self.kwargs['examanswer_pk']}))
        # return super().form_invalid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('mentor:student-exam', kwargs={'pk':self.object.exam_answer.id})

class ExamReportUpdate(UpdateView):
    model           = ExamReport
    form_class      = forms.ExamReportForm

    def form_valid(self, form):
        ins = form.instance
        form.instance.summary       = (ins.ide + ins.konsep + ins.desain + ins.proses + ins.produk) / 5
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('mentor:student-exam', kwargs={'pk':self.object.exam_answer.id}))
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('mentor:student-exam', kwargs={'pk':self.object.exam_answer.id})


