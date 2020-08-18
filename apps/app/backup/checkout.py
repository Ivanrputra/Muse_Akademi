@method_decorator([login_required], name='dispatch')
class Checkout(View):
    model = Course
    template_name   = 'app/checkout_classroom.html'

    def dispatch(self, request, *args, **kwargs):
        if Course.objects.filter(Q(session__mentor=self.request.user) | Q(admin=self.request.user)).exists():
            messages.warning(request,'Anda tidak dapat membeli kursus, karena anda terdaftar sebagai mentor atau admin pada kursus ini')
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            return HttpResponseRedirect(reverse_lazy('app:course',kwargs={'pk':self.kwargs['pk']}))   
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
            order ,created  = Order.objects.filter(~Q(status='CA')).get_or_create(course=self.object,user=request.user,price=self.object.price)
            # 'WP','CO','CA','RE','FC'
            if order.status in ['WP','RE','FC']:
                print("Ada order dalam proses pada course ini")
                return HttpResponseRedirect(reverse_lazy('app:order'))

            if created:
                invoice_new = "INV-TEST-"+ (hashlib.md5((str(order.id)+'/'+str(self.object.id)+'/'+str(self.request.user.id)).encode()).hexdigest()[:10]).upper()
                import random
                invoice_new = "INV"+ str(random.randint(0,99999999999))
                order.invoice_no = invoice_new
                order.save()
                messages.warning(request,'Berhasil menambah order')
                # messages.warning(request,'Gagal Mengambil Kelas, Kelas Berbayar, Under Development')
            else:
                messages.warning(request,'Order telah ada')
                return HttpResponseRedirect(reverse_lazy('app:order'))
        # return HttpResponseRedirect(reverse_lazy('app:course',kwargs={'pk':self.object.id}))
            # 'WP','CO','CA','RE','FC'

            # initialize snap client object
            snap = Snap(
                is_production=False,
                server_key=settings.MIDTRANS_SERVER_KEY,
                client_key=settings.MIDTRANS_CLIENT_KEY
            )

            # prepare SNAP API parameter ( refer to: https://snap-docs.midtrans.com ) minimum parameter example
            param = {
                "transaction_details": {
                    "order_id": order.invoice_no ,
                    "gross_amount": self.object.price
                },
                "item_details": [{
                    "id": str(self.object.id),
                    "price": self.object.price,
                    "quantity": 1,
                    "name": str(self.object.title+'-'+str(self.object.title)),
                    "brand": str(self.object.title),
                    "category": str('self.object.course.category.name'),
                    "merchant_name": str(self.object.admin)
                }],
                "customer_details": {
                    "first_name": request.user.firstname,
                    "last_name": request.user.lastname,
                    "email": request.user.email
                },
                "credit_card":{
                    "secure" : True
                }
            }

            # create transaction
            transaction = snap.create_transaction(param)

            # transaction token
            transaction_token = transaction['token']

            # transaction redirect url
            transaction_redirect_url = transaction['redirect_url']
            if not order.transaction_url:
                order.transaction_url = transaction_redirect_url
                order.save()
            return HttpResponseRedirect(transaction_redirect_url)
