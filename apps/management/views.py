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
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings

from core.models import MentorData,Course,Session,Exam,SessionData,Order,Library,ExamAnswer
from core.decorators import staff_required,is_staff_have
from . import forms
from core.filters import MentorDataFilter
from core.custom_mixin import CustomPaginationMixin

PAGINATE_DEFAULT = settings.PAGINATE_DEFAULT

# Create your views here.\
@method_decorator([staff_required], name='dispatch')
class Dashboard(TemplateView):
    template_name   ="management/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_siswa']  = get_user_model().objects.filter(library__course__admin=self.request.user).distinct().count()
        context['total_mentor'] = get_user_model().objects.filter(is_mentor=True).count() 
        return context


@method_decorator([staff_required], name='dispatch')
class CourseCreate(SuccessMessageMixin,CreateView):
    model           = Course
    template_name   = 'management/courses.html'
    form_class      = forms.CourseForm
    success_url     = reverse_lazy('management:courses')
    success_message = "Berhasil menambah kursus, silahkan tambahkan sesi dan publish"

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseUpdate(SuccessMessageMixin,UpdateView):
    model           = Course
    template_name   = 'management/courses.html'
    form_class      = forms.CourseUpdateForm
    success_url     = reverse_lazy('management:courses')
    success_message = "Berhasil mengupdate kursus"

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseUpdatePublish(UpdateView):
    model           = Course
    form_class      = forms.CourseUpdatePublishForm
    success_url     = reverse_lazy('management:courses')

    def form_valid(self, form,**kwargs):
        context = self.get_context_data(**kwargs)
        original_course = get_object_or_404(Course,pk=self.object.id)
        form.instance.is_publish = False if original_course.is_publish else True
        if form.instance.is_publish:
            messages.success(self.request,f'Kursus "{original_course.title}" telah berhasil dipublish')
        else:
            messages.warning(self.request,f'Kursus "{original_course.title}" telah berhasil ditarik dari publish')
        return super().form_valid(form)

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseDelete(SuccessMessageMixin,DeleteView):
    model           = Course
    success_url     = reverse_lazy('management:courses')
    success_message = "Berhasil Menghapus Kursus"

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        return context

@method_decorator([is_staff_have('Session')], name='dispatch')
class SessionCreate(SuccessMessageMixin,CreateView):
    model           = Session
    template_name   = 'management/session_create.html'
    form_class      = forms.SessionForm
    success_message = "Berhasil menambahkan sesi"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        return context

    def form_valid(self, form,**kwargs):
        context = self.get_context_data(**kwargs)
        form.instance.course = context['course']
        form = form.session_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'pk':self.object.course.id})

@method_decorator([is_staff_have('Session')], name='dispatch')
class SessionUpdate(SuccessMessageMixin,UpdateView):
    model           = Session
    template_name   = 'management/session_update.html'
    form_class      = forms.SessionForm
    success_message = "Berhasil memperbarui sesi"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_sessiondata'] = forms.SessionDataForm
        context['course'] = self.object.course
        return context
    
    def form_valid(self, form):
        form = form.session_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'pk':self.object.course.id})
    
@method_decorator([is_staff_have('Session')], name='dispatch')
class SessionDelete(SuccessMessageMixin,DeleteView):
    model           = Session
    success_message = "Berhasil menghapus sesi"
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:classroom', kwargs={'pk':self.object.course.id})

@method_decorator([is_staff_have('SessionData')], name='dispatch')
class SessionDataCreate(SuccessMessageMixin,CreateView):
    model           = SessionData
    form_class      = forms.SessionDataForm
    success_message = "Berhasil menambahkan data pada sesi"

    def form_valid(self, form):
        session = get_object_or_404(Session,pk=self.kwargs['session_pk'])
        form.instance.session = session
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:session-update', kwargs={'pk':self.object.session.id})

@method_decorator([is_staff_have('SessionData')], name='dispatch')
class SessionDataDelete(SuccessMessageMixin,DeleteView):
    model           = SessionData
    success_message = "Berhasil menghapus data sesi"
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:session-update', kwargs={'pk':self.object.session.id})

@method_decorator([is_staff_have('Course')], name='dispatch')
class CourseStudentsList(DetailView):
    model               = Course
    template_name       = "management/course_students.html"
    context_object_name = "course"

# @method_decorator([is_staff_have('ExamReport')], name='dispatch')
class ExamReport(DetailView):
    model           = ExamAnswer
    template_name   = "management/course_student_exam.html"
    context_object_name = 'exam_answer'

@method_decorator([is_staff_have('Exam')], name='dispatch')
class ExamCreate(SuccessMessageMixin,CreateView):
    model           = Exam
    template_name   = 'management/exam.html'
    form_class      = forms.ExamForm
    success_message = "Berhasil menambahkan tugas"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        return context

    def form_valid(self, form,**kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course,pk=self.kwargs['course_pk'])
        form.instance.course = context['course']
        form = form.exam_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:exam', kwargs={'course_pk':self.object.course.id})

@method_decorator([is_staff_have('Exam')], name='dispatch')
class ExamUpdate(SuccessMessageMixin,UpdateView):
    model           = Exam
    template_name   = 'management/exam_update.html'
    form_class      = forms.ExamForm
    success_message = "Berhasil memperbarui tugas"
    
    def form_valid(self, form):
        form = form.exam_date_validation()
        if not form.is_valid(): return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:exam', kwargs={'course_pk':self.object.course.id})

@method_decorator([is_staff_have('Exam')], name='dispatch')
class ExamDelete(SuccessMessageMixin,DeleteView):
    model           = Exam
    success_message = "Berhasil menghapus tugas"

    def get_success_url(self, **kwargs):         
        return reverse_lazy('management:exam', kwargs={'course_pk':self.object.course.id})

@method_decorator([staff_required], name='dispatch')
class MentorManagement(ListView):
    model               = MentorData
    template_name       = 'management/mentor_management.html'
    context_object_name = "mentor_datas"

    def get_queryset(self):
        queryset = super(MentorManagement, self).get_queryset()
        queryset = MentorDataFilter(self.request.GET, queryset=queryset).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter']       = MentorDataFilter(self.request.GET)
        return context

@method_decorator([staff_required], name='dispatch')
class MentorManagementUpdate(SuccessMessageMixin,UpdateView):
    model               = MentorData
    template_name       = 'management/mentor_management_update.html'
    form_class          = forms.RegisterMentor
    success_url         = reverse_lazy('management:mentor-management')
    context_object_name = "mentor_data"
    success_message     = "Berhasil memperbarui status pendaftaran mentor"

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
    model               = Order
    template_name       = 'management/order_management_update.html'
    form_class          = forms.OrderForm
    success_url         = reverse_lazy('management:order-management')
    context_object_name = "order"
    # success_message     = "Berhasil memperbarui status order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form']       = forms.OrderForm()
        return context

    def form_valid(self, form):
        form.instance.admin = self.request.user
        if form.instance.status == 'CO':
            messages.success(self.request,'Berhasil memperbarui status order')
            library, created = Library.objects.get_or_create(course=form.instance.course,user=form.instance.user)
        elif form.instance.status == 'DE':
            if Library.objects.filter(course=form.instance.course,user=form.instance.user).exists():
                messages.warning(self.request,'Gagal Mengubah status order, karena order telah terkonformasi sebelumnya dan library user sudah dibuat, <br> Hubungi admin muse academy untuk info lebih lanjut')
                return super().form_invalid(form)
        e
        return super().form_valid(form)
