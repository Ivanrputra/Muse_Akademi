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
from django.contrib.auth.decorators import login_required

from core.models import MentorData,Course,Library,ExamReport,ExamAnswer
from core.decorators import user_required,mentor_required,is_mentor_have
from core.custom_mixin import NoGetMixin
from . import forms

# Create your views here.\
@method_decorator([login_required], name='dispatch')
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

@method_decorator([login_required], name='dispatch')
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

@method_decorator([is_mentor_have('Course')], name='dispatch')
class CourseStudentsList(DetailView):
    model               = Course
    template_name       = "mentor/course_students.html"
    context_object_name = "course"

# @method_decorator([is_mentor_have('ExamAnswer')], name='dispatch')
# class CourseStudentExam(DetailView):
#     model               = ExamAnswer
#     template_name       = "mentor/course_student_exam.html"
#     context_object_name = "exam_answer"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reportmentor']   = ExamReport.objects.filter(mentor=self.request.user,exam_answer=self.object).first()
#         if context['reportmentor']:
#             context['form'] = forms.ExamReportForm(instance=context['reportmentor'])
#         else:
#             context['form'] = forms.ExamReportForm
#         return context

@method_decorator([is_mentor_have('ExamReport')], name='dispatch')
class ExamReportCreate(CreateView):
    model           = ExamReport
    form_class      = forms.ExamReportForm
    template_name   = "mentor/course_student_exam.html"

    def dispatch(self, request, *args, **kwargs):
        exam_report = ExamReport.objects.filter(exam_answer=self.kwargs['examanswer_pk'],mentor=self.request.user).first()
        if exam_report:
            return HttpResponseRedirect(reverse_lazy('mentor:report-update',kwargs={'pk':exam_report.id}))   
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_answer']   = get_object_or_404(ExamAnswer,pk=self.kwargs['examanswer_pk'])
        return context

    def form_valid(self, form):
        exam_answer = get_object_or_404(ExamAnswer,pk=self.kwargs['examanswer_pk'])
        form.instance.exam_answer   = exam_answer
        form.instance.mentor        = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('mentor:report-update', kwargs={'pk':self.object.id})

@method_decorator([is_mentor_have('ExamReport')], name='dispatch')
class ExamReportUpdate(UpdateView):
    model               = ExamReport
    form_class          = forms.ExamReportForm
    template_name       = "mentor/course_student_exam.html"
    context_object_name = 'exam_report'    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_answer']   = self.object.exam_answer
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('mentor:report-update', kwargs={'pk':self.object.exam_answer.id})


