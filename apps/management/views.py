from django.shortcuts import render,get_object_or_404
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django import forms
from django.urls import reverse,reverse_lazy
from django.contrib import messages

from core.models import MentorData,Course,Session,Exam,SessionData,Order,Library,ExamAnswer
from core.decorators import staff_required,is_staff_have
from . import forms


# Create your views here.\

@method_decorator([staff_required], name='dispatch')
class CourseCreate(CreateView):
    model           = Course
    template_name   = 'management/courses.html'
    form_class      = forms.CourseForm
    success_url     = reverse_lazy('management:courses')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseUpdate(UpdateView):
    model           = Course
    template_name   = 'management/courses.html'
    form_class      = forms.CourseUpdateForm
    success_url     = reverse_lazy('management:courses')

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseDelete(DeleteView):
    model       = Course
    success_url = reverse_lazy('management:courses')

@method_decorator([is_staff_have('Course')], name='dispatch')
class CoursePreview(DetailView):
    model           = Course
    template_name   = 'app/course_detail.html'

@method_decorator([is_staff_have('Course')], name='dispatch')
class ClassroomDashboard(DetailView):
    model           = Course
    template_name   = 'management/classroom.html'

@method_decorator([is_staff_have('Session')], name='dispatch')
class ClassroomSession(DetailView):
    model               = Session
    template_name       = "management/classroom_session.html"
    context_object_name = "session"

@method_decorator([is_staff_have('Session')], name='dispatch')
class SessionCreate(CreateView):
    model           = Session
    template_name   = 'management/session_create.html'
    form_class      = forms.SessionForm

    def form_valid(self, form):
        course = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        form.instance.course = course
        form = form.session_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'pk':self.object.course.id})

@method_decorator([is_staff_have('Session')], name='dispatch')
class SessionUpdate(UpdateView):
    model           = Session
    template_name   = 'management/session_update.html'
    form_class      = forms.SessionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_sessiondata'] = forms.SessionDataForm
        return context
    
    def form_valid(self, form):
        form = form.session_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'pk':self.object.course.id})
    
@method_decorator([is_staff_have('Session')], name='dispatch')
class SessionDelete(DeleteView):
    model       = Session
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'pk':self.object.course.id})

@method_decorator([is_staff_have('SessionData')], name='dispatch')
class SessionDataCreate(CreateView):
    model           = SessionData
    form_class      = forms.SessionDataForm

    def form_valid(self, form):
        session = get_object_or_404(Session,pk=self.kwargs['session_pk'])
        form.instance.session = session
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:session-update', kwargs={'pk':self.object.session.id})

@method_decorator([is_staff_have('SessionData')], name='dispatch')
class SessionDataDelete(DeleteView):
    model       = SessionData
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:session-update', kwargs={'pk':self.object.session.id})

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseStudentsList(DetailView):
    model               = Course
    template_name       = "mentor/course_students.html"
    context_object_name = "course"

# @method_decorator([is_staff_have('ExamReport')], name='dispatch')
class ExamReport(DetailView):
    model           = ExamAnswer
    template_name   = "management/course_student_exam.html"
    context_object_name = 'exam_answer'

@method_decorator([is_staff_have('Exam')], name='dispatch')
class ExamCreate(CreateView):
    model           = Exam
    template_name   = 'management/exam.html'
    form_class      = forms.ExamForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        form.instance.course = course
        form = form.exam_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:exam', kwargs={'course_pk':self.object.course.id})

@method_decorator([is_staff_have('Exam')], name='dispatch')
class ExamUpdate(UpdateView):
    model           = Exam
    template_name   = 'management/exam_update.html'
    form_class      = forms.ExamForm
    
    def form_valid(self, form):
        form = form.exam_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:exam', kwargs={'course_pk':self.object.course.id})

@method_decorator([is_staff_have('Exam')], name='dispatch')
class ExamDelete(DeleteView):
    model       = Exam
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:exam', kwargs={'course_pk':self.object.course.id})

@method_decorator([staff_required], name='dispatch')
class MentorManagement(ListView):
    model           = MentorData
    template_name   = 'management/mentor_management.html'
    context_object_name = "mentor_datas"

@method_decorator([staff_required], name='dispatch')
class MentorManagementUpdate(UpdateView):
    model           = MentorData
    template_name   = 'management/mentor_management_update.html'
    form_class      = forms.RegisterMentor
    success_url     = reverse_lazy('management:mentor-management')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        if form.instance.status == "AC":
            get_user_model().objects.filter(pk=form.instance.mentor.id).update(is_mentor=True)
        else:
            get_user_model().objects.filter(pk=form.instance.mentor.id).update(is_mentor=False)
        return super().form_valid(form)

@method_decorator([staff_required], name='dispatch')
class OrderManagement(ListView):
    model           = Order
    template_name   = 'management/order_management.html'
    context_object_name = "orders"

@method_decorator([staff_required], name='dispatch')
class OrderManagementUpdate(UpdateView):
    model           = Order
    template_name   = 'management/order_management_update.html'
    form_class      = forms.OrderForm
    success_url     = reverse_lazy('management:order-management')

    def form_valid(self, form):
        form.instance.admin = self.request.user
        print(self.object.status)
        print(form.instance.status)
        if form.instance.status == 'CO':
            messages.success(self.request,'Sukses mengupdate order')
            library, created = Library.objects.get_or_create(course=form.instance.course,user=form.instance.user)
        elif form.instance.status == 'DE':
            if Library.objects.filter(course=form.instance.course,user=form.instance.user).exists():
                messages.warning(self.request,'Gagal Mengubah status order, karena order telah terkonformasi sebelumnya dan library user sudah dibuat, <br> Hubungi admin muse academy untuk info lebih lanjut')
                return super().form_invalid(form)
        return super().form_valid(form)
