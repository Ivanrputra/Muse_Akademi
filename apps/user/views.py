# django util
from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash,get_user_model
from django.views.generic import (View,TemplateView,
								ListView,DetailView,
								CreateView,UpdateView,DeleteView)
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from core.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse,HttpResponseNotFound
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail

# python util
from . import forms
from pprint import pprint

from core.models import User

# Registration User
class register(View):
	registered = False
	template_name = 'user/registration.html'

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect("user:profile")
		user_form 		= forms.RegisterUserForm()
		return render(request, self.template_name, {'user_form': user_form,'registered':self.registered})

	def post(self, request, *args, **kwargs):
		user_form 		= forms.RegisterUserForm(data=request.POST)
		
		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.email = user.email.strip().lower()
			user.is_active = False
			user.save()
			self.registered = True

			current_site = get_current_site(request)
			mail_subject = 'Aktivasi Akun Muse Academy'
			message = render_to_string('user/acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)),
				'token':account_activation_token.make_token(user),
			})
			to_email = user_form.cleaned_data.get('email')
			send_mail(subject=mail_subject,message=message,html_message=message,from_email=None,recipient_list=[to_email])
			# email = EmailMessage(mail_subject, message, to=[to_email])
			# email.send()
			# send_mail()
			# "Muse Akademi <admin@museakademi.com>"
			messages.success(self.request,'Terima kasih sudah mendaftar, Untuk menyelesaikan pendaftaran, klik konfirmasi pada email anda')
			return render(request, self.template_name, {'user_form': user_form,'activation':'Untuk menyelesaikan pendaftaran, klik konfirmasi pada email anda'})
		else:
		    print(user_form.errors)
		return render(request, self.template_name, {'user_form': user_form,'registered':self.registered})

def user_login(request):
	if request.method == "POST":
		usernameoremail    = request.POST.get('usernameoremail').strip()
		password    = request.POST.get('password').strip()

		try:
			user = User.objects.get(Q(username=usernameoremail) | Q(email__iexact=usernameoremail))
		except User.DoesNotExist:
			messages.warning(request,'Cek email/username dan password anda lagi, atau login menggunakan google')
			return render(request,'user/login.html')
			
		if user.is_active:
			user =  authenticate(username=usernameoremail,password=password)
			if user:
				login(request,user)
				if request.POST.get('next') != '':
					return redirect(request.POST.get('next'))
				else:
					return HttpResponseRedirect(reverse_lazy('app:index'))
			else:
				messages.warning(request,'Cek email/username dan password anda atau login menggunakan google')
				return render(request,'user/login.html')
		else:
			messages.warning(request,'Akun belum teraktivasi, Cek email dan spam folder anda untuk link aktivasi akun')
			return render(request,'user/login.html')
	else:
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse('user:profile'))
		return render(request,'user/login.html',context={'next': request.GET.get('next', '')})

# Logout method
@login_required
def user_logout(request):
	logout(request)
	return redirect('user:login')

@login_required
def change_password(request):
	if request.method == 'POST':
		if request.user.has_usable_password():
			form = PasswordChangeForm(request.user, request.POST)
		else:
			form = SetPasswordForm(request.user, request.POST)

		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Password anda berhasil diganti!')
			return redirect('user:profile')
		else:
			messages.error(request, 'Perbaiki kesalahan dibawah ini.')
	else:
		if request.user.has_usable_password():
			form = PasswordChangeForm(request.user)
		else :
			form = SetPasswordForm(request.user)
	return render(request, 'user/password_change.html', {
	'form': form
	})

# path('password/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('user:password_reset_complete'),form_class=PasswordUpdateForm,template_name="user/password_change.html"),name='password_change'),	

@method_decorator([login_required], name='dispatch')
class ProfileView(SuccessMessageMixin,UpdateView):
	template_name 	= 'user/profile.html'
	model 			= get_user_model()
	form_class		= forms.ProfileUpdateForm
	success_url     = reverse_lazy('user:profile')
	success_message	= "Berhasil memperbarui Profile"
	
	def get_object(self):
		print(self.request.user.has_usable_password())
		return self.request.user

@method_decorator([login_required], name='dispatch')
class ProfilePicView(SuccessMessageMixin,UpdateView):
	template_name 	= 'user/profile_pic.html'
	model 			= get_user_model()
	success_url 	= reverse_lazy('user:profile_pic')
	form_class 		= forms.ProfilePicForm
	success_message	= "Berhasil memperbarui Gambar Profile"
	
	def get_object(self):
		return self.request.user

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = get_object_or_404(get_user_model(),pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user,backend='django.contrib.auth.backends.ModelBackend')
		messages.success(request, 'Akun anda berhasil diaktivasi')
		return HttpResponseRedirect(reverse_lazy('user:profile'))
	else:
		messages.warning(request,'Link aktivasi tidak valid atau akun telah tervalidasi')
		return HttpResponseRedirect(reverse_lazy('app:index'))
