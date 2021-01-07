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
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from core.models import Course,Session,Library,Order, \
    Exam,ExamProject,ExamAnswer,Category,Mitra,MitraUser
from core.custom_mixin import CustomPaginationMixin
from core.filters import CourseFilter
from core.decorators import is_student_have,check_exam_time,is_user_have_mitra_valid
from core.model_query import *

from . import forms

import json,os,io,hashlib

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
        context['courses_free'] = get_active_free_course()[:PAGINATE_DEFAULT]
        context['courses_partner'] = get_active_partner_course()[:PAGINATE_DEFAULT]
        return context

class CourseDetail(DetailView):
    model               = Course
    template_name       = "app/course_detail.html"
    context_object_name = "course" 

    def get_object(self):
        return get_object_or_404(Course,pk=self.kwargs['pk'],is_publish=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.object.relevant_courses)
        return context

@method_decorator([login_required], name='dispatch')
class OrderDetailUpdate(UpdateView):
    model               = Order
    template_name       = "app/order_update.html"
    context_object_name = "order" 
    form_class          = forms.OrderForm

    def form_valid(self, form):
        order = get_object_or_404(Order,pk=form.instance.id)
        if order.status == "CO":
            messages.warning(self.request,'Tidak dapat mengupdate bukti pembayaran karena status order telah terkonfirmasi, <br> Hubungi admin muse academy untuk info lebih lanjut')
            return super().form_invalid(form)
        form.instance.status = "WC"
        messages.success(self.request,"Berhasil update bukti pembayaran")
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:order-detail', kwargs={'pk':self.object.id})

class CourseList(CustomPaginationMixin,ListView):
    model               = Course
    template_name       = "app/courses_list.html"
    context_object_name = "courses"
    paginate_by         = PAGINATE_DEFAULT
    queryset            = get_active_course()

    def get_queryset(self):
        queryset = super(CourseList, self).get_queryset().filter(is_publish=True,mitra=None)
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
        form.instance.exam = get_object_or_404(Exam,pk=self.kwargs['exam_pk'])
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.id})

@method_decorator([is_student_have('ExamAnswer'),check_exam_time('ExamAnswer')], name='dispatch')
class ExamAnswerUpdate(SuccessMessageMixin,UpdateView):
    model               = ExamAnswer
    template_name       = "app/classroom_exam.html"
    form_class          = forms.ExamAnswerForm
    context_object_name = "examanswer" 
    success_message     = "Berhasil memperbarui jawaban"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam']             = self.object.exam
        context['form_examproject'] = forms.ExamProjectForm
        return context

    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.id})

@method_decorator([is_student_have('ExamProject'),check_exam_time('Exam')], name='dispatch')
class ExamProjectCreate(SuccessMessageMixin,CreateView):
    model               = ExamProject
    form_class          = forms.ExamProjectForm
    success_message     = "Berhasil menambahkan project"

    def form_valid(self, form):
        exam = get_object_or_404(Exam,pk=self.kwargs['exam_pk'])
        obj,created = ExamAnswer.objects.get_or_create(exam=exam,user=self.request.user)
        form.instance.exam_answer = obj
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request,'Gagal Menambah URL Project, Pastikan url yang anda masukkan benar')
        return HttpResponseRedirect(reverse_lazy('app:examanswer', kwargs={'exam_pk':self.kwargs['exam_pk']}))
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.exam_answer.id})

@method_decorator([is_student_have('ExamProject'),check_exam_time('ExamProject')], name='dispatch')
class ExamProjectDelete(SuccessMessageMixin,DeleteView):
    model       = ExamProject
    success_message     = "Berhasil menghapus project"
    
    def form_invalid(self, form):
        messages.warning(self.request,'Gagal Menghapus URL Project')
        return self.get_success_url()

    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:examanswer-update', kwargs={'pk':self.object.exam_answer.id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request,self.success_message) 
        return super(ExamProjectDelete, self).delete(request, *args, **kwargs)

# ttt Mitra
@method_decorator([login_required], name='dispatch')
class MitraList(ListView):
    model               = Mitra
    template_name       = "app/mitra/mitra_list.html"
    context_object_name = "mitras"

    def get_queryset(self):
        queryset = super(MitraList, self).get_queryset().filter(mitrauser__user=self.request.user).distinct()
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if Mitra.objects.filter(mitrauser__user=self.request.user).count() < 1:
            return HttpResponseRedirect(reverse_lazy('app:mitra-create'))
        return super().dispatch(request, *args, **kwargs)

@method_decorator([login_required], name='dispatch')
class MitraCreate(SuccessMessageMixin,CreateView):
    model               = Mitra
    template_name       = "app/mitra/mitra_create.html"
    form_class          = forms.MitraCreateForm
    success_message     = "Berhasil menambah mitra, admin Muse Akademi akan segera menghubungi anda"

    def get_success_url(self, **kwargs):         
        return reverse_lazy('app:mitra-list')
    
    def form_valid(self, form):
        form.instance.user_admin = self.request.user
        form.instance.save()
        mitra_user,created = MitraUser.objects.get_or_create(mitra=form.instance,user=self.request.user,is_admin=True)
        return super().form_valid(form)

@method_decorator([login_required], name='dispatch')
class MitraStatus(DetailView):
    model               = Mitra
    context_object_name = "mitra" 
    template_name       = "app/mitra/mitra_status.html"

    def dispatch(self, request, *args, **kwargs):
        mitra = get_object_or_404(self.model,pk=self.kwargs['pk'])
        if mitra.is_valid:
            return HttpResponseRedirect(reverse_lazy('app:mitra-dashboard',kwargs={'pk':mitra.id}))
        if mitra.user_admin != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

@method_decorator([login_required], name='dispatch')
class MitraDashboard(DetailView):
    model               = Mitra
    template_name       = "app/mitra/mitra_dashboard.html"
    context_object_name = "mitra" 

    def dispatch(self, request, *args, **kwargs):
        mitra = get_object_or_404(self.model,pk=self.kwargs['pk'])
        if MitraUser.objects.filter(mitra=kwargs['pk'],user=request.user).exists() or mitra.user_admin == self.request.user :
            if not mitra.is_valid:
                return HttpResponseRedirect(reverse_lazy('app:mitra-status',kwargs={'pk':mitra.id}))
            else:
                return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
        
@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsers(DetailView):
    model               = Mitra
    context_object_name = "mitra" 
    template_name       = "app/mitra/mitra_user_list.html"

@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersInvite(View):
    model = MitraUser
    
    def post(self, request, *args, **kwargs):
        mitra = get_object_or_404(Mitra,pk=self.kwargs['pk'])
        recipient_list = [email.strip().lower() for email in self.request.POST.getlist('email') if email]
        current_site = get_current_site(request)
        message = render_to_string('app/mitra/mitra_invitation.html', {
            'mitra':mitra,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(mitra.id)),
        })
        
        send_mail(subject='Undangan Kelas Mitra',message=message,html_message=message,from_email=None,recipient_list=recipient_list)
        # send_mail(subject=mail_subject,message=message,html_message=message,from_email=None,recipient_list=[to_email])
        for email  in recipient_list:
            # ttt
            invited_mitra,created = MitraInvitedUser.objects.get_or_create(mitra=mitra,email__iexact=email.strip().lower(),defaults={'invited_by':self.request.user})
        messages.success(request,"Undangan melalui email telah berhasil dikrim")
        return HttpResponseRedirect(reverse_lazy('app:mitra-users',kwargs={'pk':self.kwargs['pk']}))

@method_decorator([login_required], name='dispatch')
class MitraUsersInviteConfirm(View):
    model = MitraUser

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uidb64']))
            mitra = get_object_or_404(Mitra,pk=uid)
        except(TypeError, ValueError, OverflowError, Mitra.DoesNotExist):
            mitra = None
        if mitra:
            if MitraUser.objects.filter(user=self.request.user,mitra=mitra):
                return HttpResponseRedirect(reverse_lazy('app:mitra-dashboard',kwargs={'pk':mitra.id}))
            if mitra.max_user > MitraUser.objects.filter(mitra=mitra).count():
                if MitraInvitedUser.objects.filter(email__iexact=self.request.user.email,mitra=mitra).exists():
                    mitra_user,created = MitraUser.objects.get_or_create(mitra=mitra,user=self.request.user)
                    if created:
                        user_invited = MitraInvitedUser.objects.filter(email__iexact=self.request.user.email,mitra=mitra).first()
                        user_invited.is_confirmed = True
                        user_invited.save()
                        messages.success(request,f'Selamat anda telah tergabung pada mitra : {mitra}')
                    return HttpResponseRedirect(reverse_lazy('app:mitra-dashboard',kwargs={'pk':mitra.id}))
                else:
                    messages.warning(request,f'Email akun anda tidak terdaftar pada list undangan mitra')
            else:
                messages.warning(request,f'User Mitra yang terdaftar telah mencapai kuota maksmimal, hubungi mitra anda untuk info lebih lanjut')
        else :
            messages.warning(request,f'Link undangan mitra tidak valid')
        return HttpResponseRedirect(reverse_lazy('app:index'))

@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersUpdateStatus(View):
    model = MitraUser

    # def dispatch(self, request, *args, **kwargs):
    #     mitra_user = get_object_or_404(self.model,mitra=self.kwargs['pk'],user=self.request.user)
    #     if mitra_user.is_admin:
    #         return super().dispatch(request, *args, **kwargs)
    #     else :
    #         raise PermissionDenied
    
    def post(self, request, *args, **kwargs):
        mitra_user = get_object_or_404(self.model,pk=self.kwargs['user_pk'],mitra=self.kwargs['pk'])
        if mitra_user.is_admin:
            raise PermissionDenied
        elif mitra_user.is_co_host:
            mitra_user.is_co_host = False
            messages.success(request,f'Berhasil menghapus role user {mitra_user.user} sebagai co host')
        elif not mitra_user.is_co_host:
            mitra_user.is_co_host = True
            messages.success(request,f'Berhasil memperbarui role user {mitra_user.user} sebagai co host')
        mitra_user.save()
        return HttpResponseRedirect(reverse_lazy('app:mitra-users',kwargs={'pk':self.kwargs['pk']}))

# @method_decorator([is_user_have_mitra_valid('Mitra')], name='dispatch')
@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersDelete(View):
    model           = MitraUser

    # def dispatch(self, request, *args, **kwargs):
    #     mitra_user = get_object_or_404(self.model,mitra=self.kwargs['pk'],user=self.request.user)
    #     if mitra_user.is_admin:
    #         return super().dispatch(request, *args, **kwargs)
    #     else :
    #         raise PermissionDenied

    def post(self, request, *args, **kwargs):
        mitra_user = get_object_or_404(self.model,pk=self.kwargs['user_pk'],mitra=self.kwargs['pk'])
        if mitra_user.is_admin:
            raise PermissionDenied
        else:
            try:
                mitra_invited_email = get_object_or_404(MitraInvitedUser,email=mitra_user.user.email,mitra=self.kwargs['pk']).delete()
            except expression as identifier:
                pass
            mitra_user.delete()
        messages.success(request,f'Berhasil Menghapus Mitra User')
        return HttpResponseRedirect(reverse_lazy('app:mitra-users', kwargs={'pk':self.kwargs['pk']}))

@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersInviteMass(View):
    model = MitraUser

    def post(self, request, *args, **kwargs):
        mitra = get_object_or_404(Mitra,pk=self.kwargs['pk'])
        recipient_list = [email.strip().lower() for email in self.request.POST.get('email_list').split(';') if email]
        current_site = get_current_site(request)
        message = render_to_string('app/mitra/mitra_invitation.html', {
            'mitra':mitra,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(mitra.id)),
        })

        chunks_email = [recipient_list[x:x+50] for x in range(0, len(recipient_list), 50)]
        for email_list in chunks_email:
            send_mail(subject='Undangan Kelas Mitra',message=message,html_message=message,from_email=None,recipient_list=email_list)
        # send_mail(subject=mail_subject,message=message,html_message=message,from_email=None,recipient_list=[to_email])
        # print(chunks_email)
        # print(recipient_list)
        for email  in recipient_list:
            invited_mitra,created = MitraInvitedUser.objects.get_or_create(mitra=mitra,email__iexact=email.strip().lower(),defaults={'invited_by':self.request.user})
        messages.success(request,"Undangan melalui email telah berhasil dikrim")
        return HttpResponseRedirect(reverse_lazy('app:mitra-users',kwargs={'pk':self.kwargs['pk']}))

@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersPending(DetailView):
    model               = Mitra
    template_name       = "app/mitra/mitra_user_pending_list.html"
    context_object_name = "mitra"

@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersPendingDelete(View):
    model = MitraInvitedUser

    def post(self, request, *args, **kwargs):
        mitra_invited_email = get_object_or_404(self.model,pk=self.kwargs['invited_pk'],mitra=self.kwargs['pk'])
        mitra_invited_email.delete()
        messages.success(request,f'Berhasil Menghapus List Undangan Email Mitra')
        return HttpResponseRedirect(reverse_lazy('app:mitra-users-pending', kwargs={'pk':self.kwargs['pk']}))

@method_decorator([is_user_have_mitra_valid('AdminOrCoHost')], name='dispatch')
class MitraUsersPendingResend(View):
    model = MitraInvitedUser

    def post(self, request, *args, **kwargs):
        mitra_invited_email = get_object_or_404(self.model,pk=self.kwargs['invited_pk'],mitra=self.kwargs['pk'])
        mitra_invited_email.resend_by = self.request.user
        mitra_invited_email.save()
        recipient_list = [mitra_invited_email.email]
        current_site = get_current_site(request)
        message = render_to_string('app/mitra/mitra_invitation.html', {
            'mitra':mitra_invited_email.mitra,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(mitra_invited_email.mitra.id)),
        })
        
        send_mail(subject='Undangan Kelas Mitra',message=message,html_message=message,from_email=None,recipient_list=recipient_list)
        messages.success(request,f'Berhasil Mengirim Ulang Undangan ke alamat email : {mitra_invited_email.email}')
        return HttpResponseRedirect(reverse_lazy('app:mitra-users-pending', kwargs={'pk':self.kwargs['pk']}))

@method_decorator([is_user_have_mitra_valid('Mitra')], name='dispatch')
class MitraCourses(DetailView):
    model               = Mitra
    template_name       = "app/mitra/mitra_course_list.html"
    context_object_name = "mitra"

# /ttt Mitra

@method_decorator([login_required], name='dispatch')
class Checkout(View):
    model = Course
    template_name   = 'app/checkout_classroom.html'

    def dispatch(self, request, *args, **kwargs):
        # messages.warning(request,'Anda tidak dapat membeli kursus, karena anda terdaftar sebagai mentor atau admin pada kursus ini')
        # return HttpResponseRedirect(reverse_lazy('app:course',kwargs={'pk':self.kwargs['pk']}))   
        course = Course.objects.filter(pk=self.kwargs['pk']).filter(Q(session__mentor=self.request.user) | Q(admin=self.request.user)).first()
        if course:
            messages.warning(request,f'Anda terdaftar sebagai mentor pada kursus {course}')
            return HttpResponseRedirect(reverse_lazy('mentor:classroom',kwargs={'pk':self.kwargs['pk']}))
            
        lib = Library.objects.filter(user=self.request.user,course=self.kwargs['pk']).first()
        if lib:
            messages.success(request,'Anda sudah memiliki kelas ini')
            return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':lib.id}))   
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.course = get_object_or_404(self.model,pk=self.kwargs['pk'])

        # Mitra Class

        if self.course.mitra and self.course.is_publish:
            mitra_user = MitraUser.objects.filter(user=self.request.user,mitra=self.course.mitra).exists()
            if mitra_user:
                new_lib = Library(course=self.course,user=self.request.user)
                new_lib.save()
                messages.success(request,'Berhasil Mengambil Kelas Mitra')
                return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':new_lib.id}))
            else:
                messages.warning(request,'Anda Tidak Terdaftar Pada Kelas Mitra Ini')
                return HttpResponseRedirect(reverse_lazy('app:index'))

        # /Mitra Class

        if self.course.start_at < timezone.now().date():
            messages.warning(request,'Kelas Sudah dimulai, anda tidak dapat mengambil kelas ini')
            return HttpResponseRedirect(reverse_lazy('app:index'))

        if not self.course.is_publish:
            messages.warning(request,'Kelas tidak di publish')
            return HttpResponseRedirect(reverse_lazy('app:index'))

        if self.course.is_free():
            new_lib = Library(course=self.course,user=self.request.user)
            new_lib.save()
            messages.success(request,'Berhasil Mengambil Kelas Gratis')
            return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':new_lib.id}))
        else:
            order ,created  = Order.objects.get_or_create(course=self.course,user=request.user,price=self.course.price,discount=self.course.discount)

            if created:
                # invoice_new = "INV-TEST-"+ (hashlib.md5((str(order.id)+'/'+str(self.course.id)+'/'+str(self.request.user.id)).encode()).hexdigest()[:10]).upper()
                # import random
                invoice_new         = f'INV-{order.user.id}-{self.course.id}-{order.id}'
                order.invoice_no    = invoice_new
                order.save()
                messages.success(request,'Berhasil menambah order')
            else:
                if order.status in ['WP']:
                    messages.info(request,'Anda telah memesan kursus ini sebelumnya, segera selesaikan pembayaran')
                elif order.status in ['WC']:
                    messages.info(request,'Anda telah memesan kursus ini sebelumnya, mohon tunggu konfirmasi pembayaran')
                elif order.status in ['CO']:
                    messages.info(request,'Pesanan anda pada kursus ini telah dikonfirmasi')
            return HttpResponseRedirect(reverse_lazy('app:order-detail',kwargs={'pk':order.id}))

@method_decorator([is_student_have('Library')], name='dispatch')
class CertificatePDFView(View):
    def get(self, request, *args, **kwargs):
        library = get_object_or_404(Library,course=kwargs['course_pk'],user=self.request.user)
        
        is_free = True if library.course.is_free() else False

        if not is_free:

            if library.summary != None:
                if library.summary < settings.NILAI_SKM:
                    messages.warning(request,"Hasil Summary anda dibawah rata-rata")
                    return HttpResponseRedirect(reverse_lazy('app:library'))
            else:
                messages.warning(request,"Tunggu sampai hasil penilaian keluar")
                return HttpResponseRedirect(reverse_lazy('app:library'))      
            
        template = get_template("certificate.html")
        html = template.render({'pagesize':'A4','user':request.user,'course':library.course,'is_free':is_free})
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

