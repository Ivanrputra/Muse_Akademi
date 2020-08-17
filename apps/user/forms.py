from django import forms
from django.core import validators

from string import Template
from django.utils.safestring import mark_safe

from django.contrib.auth import get_user_model,authenticate,password_validation
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.forms.widgets import ClearableFileInput
from croppie.fields import CroppieField
from django.utils.translation import gettext, gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

# Form for user registration
class RegisterUserForm(UserCreationForm):
    firstname   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Nama Depan'}),
        label = _("Nama Depan Label")
    )
    lastname    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Nama Belakang'}))
    username    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Username'}))
    email       = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Email'}))
    password1   = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control text-dark','placeholder':'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control text-dark','placeholder':'Konfirmasi Password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta():
        model 	= get_user_model()
        fields 	= ('firstname','lastname','username','email')

class ProfilePicForm(forms.ModelForm):
	profile_pic = CroppieField(
		options={
            'viewport': {
                'width': 175,
                'height': 175,
            },
            'boundary': {
                'width': 225,
                'height': 225,
            },
            'showZoomer': True,
        },
	)
	
	class Meta():
		model 	= get_user_model() 
		fields = ('profile_pic',)

class ProfileUpdateForm(forms.ModelForm):
    firstname   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nama Depan'}),
        label = _("Nama Depan")
    )
    lastname   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nama Belakang'}),
        label = _("Nama Belakang")
    )
    username   = forms.CharField(min_length=8,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nama Pengguna'}),
        label = _("Nama Pengguna")
    )
    phone   = PhoneNumberField(min_length=10, max_length=15, widget=forms.TextInput(attrs={'class':'form-control','type':'number','placeholder':'No. Telepon'}),
        label = _("No. Telepon")
    )
    address   = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Alamat'}),
        label = _("Alamat")
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username.split(' ')) > 1:
            raise forms.ValidationError(_('Username tidak boleh ada spasi')) 
        if len(username) < 8:
            raise forms.ValidationError(_('minimal karakter adalah 8')) 
        user = get_user_model().objects.filter(username=username).exclude(pk=self.instance.id).exists()
        if user:
            raise forms.ValidationError('Username '+username+' tidak tersedia') 
        return username

    class Meta():
        model 	= get_user_model() 
        fields  = ('username','firstname','lastname','phone','address')

class PasswordUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Kata Sandi Lama"),
        widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete': 'current-password', 'autofocus': True}),
    )
    new_password1 = forms.CharField(
        label=_("Kata Sandi Baru"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Ulangi Kata Sandi"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'autofocus': True}),
        
    )