from django.urls import path
from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import PasswordUpdateForm

app_name = 'user'

urlpatterns = [
	# USER LOGIN AND REGISTRATION
	path('login/', views.user_login,name='login'),
	path('register/', views.register.as_view(),name='register'),
	path('activate/<str:uidb64>/<str:token>/',views.activate, name='activate'),

	# # NEED LOGIN USER
	path('profile/', views.ProfileView.as_view(),name='profile'),
	path('profile_pic/', views.ProfilePicView.as_view(),name='profile_pic'),
	path('logout/', views.user_logout,name='logout'),

	# path('password/', views.change_password, name='change_password'),
	path('password/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('user:password_reset_complete'),form_class=PasswordUpdateForm,template_name="user/password_change.html"),name='password_change'),	
	path('reset/complete',auth_views.PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"),name='password_reset_complete'),	


	path('password/reset/',auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('user:password_reset_done'),
        email_template_name="user/password_reset_mail.html",
        template_name="user/password_reset.html"),
        name='password_reset'),	
	path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name="user/password_reset_done.html"),
        name='password_reset_done'),	
    path('password/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('user:password_reset_complete'),
        template_name="user/password_reset_confirm.html"),
        name='password_reset_confirm'),	
	
# template_name="user/change_password.html"),
	# accounts/login/ [name='login']
	# accounts/logout/ [name='logout']
	# accounts/password_change/ [name='password_change']
	# accounts/password_change/done/ [name='password_change_done']
	# accounts/password_reset/ [name='password_reset']
	# accounts/password_reset/done/ [name='password_reset_done']
	# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
	# accounts/reset/done/ [name='password_reset_complete']
]
