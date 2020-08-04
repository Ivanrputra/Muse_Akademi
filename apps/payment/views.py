from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)

import json,jsonify
from midtransclient import Snap, CoreApi

from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse,QueryDict,StreamingHttpResponse
from django.db import transaction
from django.contrib import messages
from django.urls import reverse,reverse_lazy
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash,get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from core.models import Order,Library,Course

core = CoreApi(
    is_production=False,
    server_key=settings.MIDTRANS_SERVER_KEY,
    client_key=settings.MIDTRANS_CLIENT_KEY
)

# Create your views here.
@method_decorator([csrf_exempt,transaction.atomic], name='dispatch')
class notification_handler(View):

    def post(self, request, *args, **kwargs):
        
        # request_json = request.get_json()
        request_json            =  json.loads(request.body)
        transaction_status_dict = core.transactions.notification(request_json)
        print(request_json)
        order_id                = request_json['order_id']
        print(order_id)
        transaction_status      = request_json['transaction_status']
        print(transaction_status)
        
        transaction_json        = json.dumps(transaction_status_dict)
        fraud_status            = None
        order = get_object_or_404(Order,invoice_no=order_id)
        # [5.B] Handle transaction status on your backend
        # Sample transaction_status handling logic
        if transaction_status == 'capture':
            fraud_status       = request_json['fraud_status']
            if fraud_status == 'challenge':
                # TODO set transaction status on your databaase to 'challenge'
                order.status = 'FC'
            elif fraud_status == 'accept':
                # TODO set transaction status on your databaase to 'success'
                order.status = 'CO'
                # messages.success()
                # new_lib = CourseLibrary(classroom=get_object_or_404(Classroom,pk=order.classroom),user=get_object_or_404(get_user_model(),pk=order.user))
                new_lib,created = Library.objects.get_or_create(course=get_object_or_404(Course,pk=order.course.id),user=get_object_or_404(get_user_model(),pk=order.user.id))
        elif transaction_status == 'settlement':
            # TODO set transaction status on your databaase to 'success'
            # Note: Non card transaction will become 'settlement' on payment success
            # Credit card will also become 'settlement' D+1, which you can ignore
            # because most of the time 'capture' is enough to be considered as success
            order.status = 'CO'
            # messages.success()
            # new_lib = CourseLibrary(classroom=get_object_or_404(Classroom,pk=.id),user=order.user)
            new_lib,created = Library.objects.get_or_create(course=get_object_or_404(Course,pk=order.course.id),user=get_object_or_404(get_user_model(),pk=order.user.id))
        elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
            # TODO set transaction status on your databaase to 'failure'
            order.status = 'CA'
        elif transaction_status == 'pending':
            # TODO set transaction status on your databaase to 'pending' / waiting payment
            order.status = 'WP'
        elif transaction_status == 'refund':
            # TODO set transaction status on your databaase to 'refund'
            order.status = 'RE'
        # app.logger.info(summary)
        order.save()
        summary = 'Transaction notification received. Order ID: {order_id}. Transaction status: {transaction_status}. Fraud status: {fraud_status}.<br>Raw notification object:<pre>{transaction_json}</pre>'.format(order_id=order_id,transaction_status=transaction_status,fraud_status=fraud_status,transaction_json=transaction_json)
        print(summary)
        
        return JsonResponse(summary,safe=False)
        # return HttpResponseRedirect(reverse_lazy('app:order'))

@method_decorator([login_required,transaction.atomic], name='dispatch')
class finish(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('transaction_status') == 'capture':
            messages.success(request,"Your order is waiting for captured")
        elif request.GET.get('transaction_status') == 'settlement':
            messages.success(request,"Your order has been confirmed")
        elif request.GET.get('transaction_status') == 'pending':
            messages.success(request,"Your order is waiting for payment")
        return HttpResponseRedirect(reverse_lazy('app:order'))

@method_decorator([login_required,transaction.atomic], name='dispatch')
class unfinish(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order,invoice_no=request.GET.get('order_id'))
        if order.status == 'OC':
            order.delete()
        messages.warning(request,"Your order is Canceled")
        
        return HttpResponseRedirect(reverse_lazy('app:order'))

@method_decorator([login_required,transaction.atomic], name='dispatch')
class error(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order,invoice_no=request.GET.get('order_id'))
        if order.status == 'OC':
            order.delete()
        messages.warning(request,"Your order Denied or Error")
        return HttpResponseRedirect(reverse_lazy('app:order'))