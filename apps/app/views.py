from django.shortcuts import render,get_object_or_404,redirect
from django.http import (HttpResponseRedirect, HttpResponse,HttpResponseNotFound,
                        QueryDict,StreamingHttpResponse,FileResponse,Http404)
from django.views.generic.base import RedirectView
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
								CreateView,UpdateView,
                                DeleteView)
from django.views.generic.edit import DeletionMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import get_template,render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.utils import timezone

from core.models import Course,Session,Library,Order, \
    Exam,ExamProject,ExamAnswer,Category
from core.custom_mixin import CustomPaginationMixin
from core.filters import CourseFilter
from core.decorators import is_student_have,check_exam_time
from core.model_query import *

from . import forms

import json,os,io,hashlib
# from datetime import datetime
# Payment
from midtransclient import Snap, CoreApi
# PDF GENERATOR
from xhtml2pdf import pisa 

# Create your views here.
PAGINATE_DEFAULT = settings.PAGINATE_DEFAULT

def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = ''
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path+request.POST.get('next'))
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response

class IndexView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']   = Category.objects.all()[:8]
        context['courses']      = get_active_course()[:PAGINATE_DEFAULT]
        return context

class CourseDetail(DetailView):
    model               = Course
    template_name       = "app/course_detail.html"
    context_object_name = "course" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator([login_required], name='dispatch')
class OrderDetail(UpdateView):
    model               = Order
    template_name       = "app/order_update.html"
    context_object_name = "order" 
    form_class          = forms.OrderForm

    def form_valid(self, form):
        form.instance.status = "WC"
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:order-detail', kwargs={'pk':self.object.id})

class CourseList(ListView,CustomPaginationMixin):
    model               = Course
    template_name       = "app/courses_list.html"
    context_object_name = "courses"
    paginate_by         = PAGINATE_DEFAULT
    queryset            = get_active_course()

    def get_queryset(self):
        # queryset = super(CourseList, self).get_queryset().filter(is_publish=True)
        queryset = super(CourseList, self).get_queryset()
        queryset = CourseFilter(self.request.GET, queryset=queryset).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']   = Category.objects.all()
        context['filter']       = CourseFilter(self.request.GET)
        return context

class ClassroomRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        library = get_object_or_404(Library, course=kwargs['pk'],user=self.request.user)
        return reverse('app:dashboard-classroom', kwargs={'pk':library.id})

@method_decorator([is_student_have('Library')], name='dispatch')
class DashboardClassroom(DetailView):
    model               = Library
    template_name       = "app/dashboard_classroom.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course']   = self.object.course
        return context

@method_decorator([is_student_have('Session')], name='dispatch')
class ClassroomSession(DetailView):
    model               = Session
    template_name       = "app/classroom_session.html"
    context_object_name = "session"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course']   = self.object.course
        return context


@method_decorator([is_student_have('Library')], name='dispatch')
class ClassroomExams(DetailView):
    model               = Library
    template_name       = "app/classroom_exams.html"
    context_object_name = "library"

    def get_object(self):
        return Library.objects.get(user=self.request.user,course=self.kwargs['course_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course']   = self.object.course
        return context

@method_decorator([is_student_have('ExamAnswer'),check_exam_time('Exam')], name='dispatch')
class ExamAnswerCreate(CreateView):
    model           = ExamAnswer
    template_name   = "app/classroom_exam.html"
    form_class      = forms.ExamAnswerForm

    def dispatch(self, request, *args, **kwargs):
        exam_answer = ExamAnswer.objects.filter(user=self.request.user,exam=self.kwargs['exam_pk']).first()
        if exam_answer:
            return redirect(reverse_lazy('app:examanswer-update',kwargs={'pk':exam_answer.id}),permanent=True)   

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam']      = get_object_or_404(Exam,pk=self.kwargs['exam_pk'])
        context['form_examproject'] = forms.ExamProjectForm
        return context

    def form_valid(self, form):
        exam = get_object_or_404(Exam,pk=self.kwargs['exam_pk'])
        form.instance.exam = exam
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.id})

@method_decorator([is_student_have('ExamAnswer'),check_exam_time('ExamAnswer')], name='dispatch')
class ExamAnswerUpdate(UpdateView):
    model               = ExamAnswer
    template_name       = "app/classroom_exam.html"
    form_class          = forms.ExamAnswerForm
    context_object_name = "examanswer" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam']             = self.object.exam
        context['form_examproject'] = forms.ExamProjectForm
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.id})

@method_decorator([is_student_have('ExamProject'),check_exam_time('Exam')], name='dispatch')
class ExamProjectCreate(CreateView):
    model               = ExamProject
    form_class          = forms.ExamProjectForm

    def form_valid(self, form):
        exam = get_object_or_404(Exam,pk=self.kwargs['exam_pk'])
        obj,created = ExamAnswer.objects.get_or_create(exam=exam,user=self.request.user)
        form.instance.exam_answer = obj
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request,'Gagal Menambah Data Project, Pastikan file project tidak melebihi 10MB')
        return HttpResponseRedirect(reverse_lazy('app:examanswer', kwargs={'exam_pk':self.kwargs['exam_pk']}))
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.exam_answer.id})

@method_decorator([is_student_have('ExamProject'),check_exam_time('ExamProject')], name='dispatch')
class ExamProjectDelete(DeleteView):
    model       = ExamProject
    
    def form_invalid(self, form):
        messages.warning(self.request,'Gagal Menghapus Project')
        return self.get_success_url()

    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.exam_answer.id})

@method_decorator([login_required], name='dispatch')
class Checkout(View):
    model = Course
    template_name   = 'app/checkout_classroom.html'

    def dispatch(self, request, *args, **kwargs):
        # if Course.objects.filter(Q(session__mentor=self.request.user) | Q(admin=self.request.user)).exists():
        #     messages.warning(request,'Anda tidak dapat membeli kursus, karena anda terdaftar sebagai mentor atau admin pada kursus ini')
        #     return HttpResponseRedirect(reverse_lazy('app:course',kwargs={'pk':self.kwargs['pk']}))   
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        lib = Library.objects.filter(user=self.request.user,course=self.kwargs['pk']).first()
        if lib:
            messages.success(request,'Anda sudah memiliki kelas ini')
            return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':lib.id}))   
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model,pk=self.kwargs['pk'])

        if not self.object.is_publish:
            messages.warning(request,'Kelas Belum Publish')
            return HttpResponseRedirect(reverse_lazy('app:index'))

        if self.object.is_free():
            new_lib = Library(course=self.object,user=self.request.user)
            new_lib.save()
            messages.success(request,'Berhasil Mengambil Kelas Gratis')
            return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':new_lib.id}))
        else:
            order ,created  = Order.objects.get_or_create(course=self.object,user=request.user,price=self.object.price)

            if created:
                # invoice_new = "INV-TEST-"+ (hashlib.md5((str(order.id)+'/'+str(self.object.id)+'/'+str(self.request.user.id)).encode()).hexdigest()[:10]).upper()
                # import random
                invoice_new = f'INV-{order.user.id}-{self.object.id}-{order.id}'
                print(invoice_new)
                order.invoice_no = 'asdasdasdd'
                order.save()
                messages.warning(request,'Berhasil menambah order')
                # messages.warning(request,'Gagal Mengambil Kelas, Kelas Berbayar, Under Development')

            if order.status in ['WP','WC','CO']:
                print("Ada order dalam proses pada course ini")
                return HttpResponseRedirect(reverse_lazy('app:order'))

            return HttpResponseRedirect(reverse_lazy('app:order-detail',kwargs={'pk':self.object.id}))

@method_decorator([is_student_have('Library')], name='dispatch')
class CertificatePDFView(View):
    def get(self, request, *args, **kwargs):
        library = get_object_or_404(Library,pk=kwargs['library_pk'])
        
        if library.summary != None:
            if library.summary < settings.NILAI_SKM:
                messages.warning(request,"Hasil Summary anda dibawah rata-rata")
                return HttpResponseRedirect(reverse_lazy('app:index'))
        else:
            messages.warning(request,"Tunggu sampai hasil penilaian keluar")
            return HttpResponseRedirect(reverse_lazy('app:index'))
            
        template = get_template("certificate.html")
        html = template.render({'pagesize':'A4','user':request.user,'course':library.course})
        result = io.BytesIO() 
        pdf = pisa.pisaDocument(io.BytesIO(html.encode('ISO-8859-1')), dest=result
            ,link_callback=fetch_resources)
        if not pdf.err: return HttpResponse(result.getvalue(), content_type='application/pdf') 
        else: return HttpResponse('Errors')

def fetch_resources(uri, rel):
    return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

def page_not_found(request,exception=None):
    return render(request, '404.html')

def page_permission_denied(request,exception=None):
    return render(request, '403.html')
