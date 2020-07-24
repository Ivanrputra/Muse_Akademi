from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model,authenticate

from string import Template

from core.models import MentorData

# Form for user registration
class RegisterMentor(forms.ModelForm):

	class Meta():
		model 	= MentorData
		fields 	= ('cv','ktp','npwp','certification','portofolio')