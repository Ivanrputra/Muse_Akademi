from django import forms
from django.core import validators

from string import Template
from django.utils.safestring import mark_safe

from django.contrib.auth import get_user_model,authenticate,password_validation
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput
from croppie.fields import CroppieField
from django.utils.translation import gettext, gettext_lazy as _

# Form for user registration
class RegisterUserForm(UserCreationForm):
    firstname   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Nama Depan'}),
        label = _("Nama Depan Label")
    )
    lastname    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Nama Belakang'}))
    username    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Username'}))
    email       = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control text-dark','placeholder':'Email'}))
    password1 = forms.CharField(
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

	class Meta():
		model 	= get_user_model() 
		fields  = ('firstname','lastname',)