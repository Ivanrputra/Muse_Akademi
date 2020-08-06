from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model,authenticate

from string import Template

from core.models import MentorData,ExamReport

# Form for user registration
class RegisterMentor(forms.ModelForm):
	class Meta():
		model 	= MentorData
		fields 	= ('cv','ktp','npwp','certification','portofolio')

class ExamReportForm(forms.ModelForm):
	ide		= forms.IntegerField(min_value=0,max_value=100,
		error_messages = {'min_value': 'Your Email Confirmation Not Equal With Your Email'}
	)
	konsep	= forms.IntegerField(min_value=0,max_value=100)
	desain	= forms.IntegerField(min_value=0,max_value=100)
	proses	= forms.IntegerField(min_value=0,max_value=100)
	produk	= forms.IntegerField(min_value=0,max_value=100)

	class Meta():
		model 	= ExamReport
		fields 	= ('ide','konsep','desain','proses','produk',)