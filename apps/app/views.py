from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseNotFound,QueryDict,StreamingHttpResponse,FileResponse,Http404
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
								CreateView,UpdateView,DeleteView)
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from core.models import Course,Session,Library,Order

# Create your views here.

class IndexView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CourseDetail(DetailView):
    model               = Course
    template_name       = "app/course_detail.html"
    context_object_name = "course" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CourseList(ListView):
    model               = Course
    template_name       = "app/courses_list.html"
    context_object_name = "courses"

class DashboardClassroom(DetailView):
    model               = Library
    template_name       = "app/dashboard_classroom.html"
    context_object_name = "library"

class ClassroomSession(DetailView):
    model               = Session
    template_name       = "app/classroom_session.html"
    context_object_name = "session"

class Checkout(View):
    model = Course
    template_name   = 'app/checkout_classroom.html'

    def dispatch(self, request, *args, **kwargs):
        lib = Library.objects.filter(user=self.request.user,course=self.kwargs['pk']).first()
        if lib:
            messages.success(request,'Anda sudah memiliki kelas ini')
            return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':lib.id}))   
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model,pk=self.kwargs['pk'])
        if self.object.is_free():
            new_lib = Library(course=self.object,user=self.request.user)
            new_lib.save()
            messages.success(request,'Berhasil Mengambil Kelas Gratis')
            return HttpResponseRedirect(reverse_lazy('app:dashboard-classroom',kwargs={'pk':new_lib.id}))
        else:
            order ,created  = Order.objects.get_or_create(course=self.object,user=request.user,price=self.object.price)
            # 'WP','CO','CA','RE','FC'
            if order.status in ['WP','RE','FC']:
                print("There is on progress Transaction in this classroom")
                return HttpResponseRedirect(reverse_lazy('app:order'))

            if created:
                # invoice_new = "INV-TEST-"+ (hashlib.md5((str(order.id)+'/'+str(self.object.id)+'/'+str(self.request.user.id)).encode()).hexdigest()[:10]).upper()
                # import random
                # invoice_new = "INV"+ str(random.randint(0,99999999999))
                # order.invoice_no = invoice_new
                # order.save()
                messages.warning(request,'Berhasil menambah order')
                # messages.warning(request,'Gagal Mengambil Kelas, Kelas Berbayar, Under Development')
            else:
                messages.warning(request,'Order telah ada')
                return HttpResponseRedirect(reverse_lazy('app:order'))
        return HttpResponseRedirect(reverse_lazy('app:course',kwargs={'pk':self.object.id}))

def page_not_found(request,exception=None):
    return render(request, '404.html')

def page_permission_denied(request,exception=None):
    return render(request, '403.html')
