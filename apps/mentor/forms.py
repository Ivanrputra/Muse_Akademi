from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model,authenticate
from django.forms.widgets import ClearableFileInput

from string import Template

from core.models import MentorData,ExamReport

class CustomClearableFileInput(ClearableFileInput):
	template_name = "ext/input_group_file.html"

# Form for user registration
class RegisterMentor(forms.ModelForm):
	ktp		= forms.FileField(widget=CustomClearableFileInput(attrs={}))
	class Meta():
		model 	= MentorData
		fields 	= ('no_ktp','ktp','certification','cv','npwp','portofolio')

class ExamReportForm(forms.ModelForm):
	ide		= forms.IntegerField(min_value=0,max_value=100)
	konsep	= forms.IntegerField(min_value=0,max_value=100)
	desain	= forms.IntegerField(min_value=0,max_value=100)
	proses	= forms.IntegerField(min_value=0,max_value=100)
	produk	= forms.IntegerField(min_value=0,max_value=100)
	# 	,error_messages = {'min_value': 'Your Email Confirmation Not Equal With Your Email'}
	# )
	class Meta():
		model 	= ExamReport
		fields 	= ('ide','konsep','desain','proses','produk',)