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
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings


from core.models import MentorData,Course,Library,ExamReport,ExamAnswer,Session
from core.decorators import user_required,mentor_required,is_mentor_have
from core.custom_mixin import CustomPaginationMixin
from core.filters import CourseFilter

from . import forms

PAGINATE_DEFAULT = settings.PAGINATE_DEFAULT

# Create your views here.\
@method_decorator([login_required], name='dispatch')
class MentorRegister(SuccessMessageMixin,CreateView):
    model           = MentorData
    template_name   = 'mentor/registration.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('mentor:register')
    success_message = "Berhasil mendaftar sebagai mentor, tunggu konfirmasi dari admin Muse Academy"

    def form_valid(self, form):
        form.instance.mentor = self.request.user
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        mentor_data = self.model.objects.filter(mentor=self.request.user).first()
        if mentor_data:
            return HttpResponseRedirect(reverse_lazy('mentor:register-update',kwargs={'pk':mentor_data.id}))
        return super().dispatch(request, *args, **kwargs)

@method_decorator([login_required], name='dispatch')
class MentorRegisterUpdate(SuccessMessageMixin,UpdateView):
    model           = MentorData
    template_name   = 'mentor/registration.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('mentor:register')
    success_message = "Berhasil memperbarui data mentor"

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
class ClassroomExams(DetailView):
    model               = Course
    template_name       = "mentor/classroom_exams.html"
    context_object_name = "course"

@method_decorator([is_mentor_have('Course')], name='dispatch')
class CourseStudentsList(DetailView):
    model               = Course
    template_name       = "mentor/course_students.html"
    context_object_name = "course"

@method_decorator([mentor_required], name='dispatch')
class MentorCourses(CustomPaginationMixin,ListView):
    model               = Course
    template_name       = "mentor/courses.html"
    context_object_name = "courses"
    paginate_by         = PAGINATE_DEFAULT
    
    def get_queryset(self):
        queryset = super(MentorCourses, self).get_queryset()
        queryset = self.request.user.mentor_courses()
        queryset = CourseFilter(self.request.GET, queryset=queryset).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter']       = CourseFilter(self.request.GET)
        return context

@method_decorator([is_mentor_have('ExamReport')], name='dispatch')
class ExamReportCreate(SuccessMessageMixin,CreateView):
    model           = ExamReport
    form_class      = forms.ExamReportForm
    template_name   = "mentor/course_student_exam.html"
    success_message = "Berhasil memberi penilaian"

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
class ExamReportUpdate(SuccessMessageMixin,UpdateView):
    model               = ExamReport
    form_class          = forms.ExamReportForm
    template_name       = "mentor/course_student_exam.html"
    context_object_name = 'exam_report'    
    success_message     = "Berhasil memperbarui penilaian"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam_answer']   = self.object.exam_answer
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('mentor:report-update', kwargs={'pk':self.object.id})

@method_decorator([is_mentor_have('Course')], name='dispatch')
class MentorClassroom(DetailView):
    model               = Course
    template_name       = "mentor/classroom.html"
    context_object_name = "course"

@method_decorator([is_mentor_have('Session')], name='dispatch')
class ClassroomSession(DetailView):
    model               = Session
    template_name       = "mentor/classroom_session.html"
    context_object_name = "session"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course']   = self.object.course
        return context