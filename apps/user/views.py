# django util
from django.shortcuts import render,redirect,get_object_or_404
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
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return render(request, self.template_name, {'user_form': user_form,'activation':'Please confirm your email address to complete the registration'})
		else:
		    print(user_form.errors)
		return render(request, self.template_name, {'user_form': user_form,'registered':self.registered})

def user_login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('user:profile'))
	
	if request.method == "POST":
		usernameoremail    = request.POST.get('usernameoremail')
		password    = request.POST.get('password')

		try:
			# user = User.objects.get(email=email)
			# user = User.objects.get(username=username)
			user = User.objects.get(Q(username=usernameoremail) | Q(email=usernameoremail))
		except User.DoesNotExist:
			return render(request,'user/login.html',{'error':'Check your email/username and password again'})
			
		if user.is_active:
			user =  authenticate(username=usernameoremail,password=password)
			print('1')
			if user:
				print('2')
				login(request,user)
				if request.POST.get('next'):
					print('3')
					return HttpResponseRedirect(request.POST.get('next'))
				else:
					print('4')
					return HttpResponseRedirect(reverse('user:profile'))
			else:
				print('5')
				return render(request,'user/login.html',{'error':'Check your email and password again'})
		else:
			print('6')
			return render(request,'user/login.html',{'error':'User account is not activated yet, Please check your email'})
	else:
		print('7')
		return render(request,'user/login.html',context={'next': request.GET.get('next', '')})


# Logout method
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('user:profile'))

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
			messages.success(request, 'Your password was successfully updated!')
			return redirect('user:profile')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		if request.user.has_usable_password():
			form = PasswordChangeForm(request.user)
		else :
			form = SetPasswordForm(request.user)
	return render(request, 'user/change_password.html', {
	'form': form
	})

@method_decorator([login_required], name='dispatch')
class ProfileView(UpdateView):
	template_name 	= 'user/profile.html'
	model 			= get_user_model()
	fields          = ('firstname','lastname','profile_pic')
	success_url     = reverse_lazy('user:profile')
	
	def get_object(self):
		return self.request.user

@method_decorator([login_required], name='dispatch')
class ProfilePicView(UpdateView,FormMixin):
	template_name 	= 'user/profile_pic.html'
	model 			= get_user_model()
	success_url = reverse_lazy('user:profile_pic')
	form_class = forms.ProfilePicForm
	
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
		return HttpResponseRedirect(reverse_lazy('app:profile'))
	else:
		return HttpResponse('Link aktivasi tidak valid')
