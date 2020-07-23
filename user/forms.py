from django import forms
from django.core import validators

from string import Template
from django.utils.safestring import mark_safe

from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import ClearableFileInput
# from croppie.fields import CroppieField

# Form for user registration
class RegisterUserForm(UserCreationForm):

	class Meta():
		model 	= get_user_model()
		fields 	= ('firstname','lastname','username','email')