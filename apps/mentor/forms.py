from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model,authenticate
from django.forms.widgets import ClearableFileInput

from string import Template

from core.models import MentorData,ExamReport,Evaluation

class CustomClearableFileInput(ClearableFileInput):
	template_name = "ext/input_group_file.html"

class ProfileUpdateForm(forms.ModelForm):
	headline	= forms.CharField(required=True)
	biography	= forms.CharField(required=True,widget=forms.Textarea())

	class Meta():
		model 	= MentorData
		fields 	= ('headline','biography',)

# Form for user registration
class RegisterMentor(forms.ModelForm):
	no_ktp   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nomor Kartu Tanda Penduduk'}),
        label = "Nomor KTP"
    )
	ktp		= forms.FileField(widget=CustomClearableFileInput(attrs={'placeholder':'JPG Maks 100 KB'}),
		label = "Scan KTP"
	)
	certification = forms.FileField(widget=CustomClearableFileInput(attrs={'placeholder':'PDF Maks 100 KB'}),
		label = "File Sertifikasi"
	)
	cv = forms.FileField(widget=CustomClearableFileInput(attrs={'placeholder':'PDF Maks 100 KB'}),
		label = "File CV"
	)
	npwp = forms.FileField(widget=CustomClearableFileInput(attrs={'placeholder':'PDF Maks 100 KB'}),
		label = "File NPWP"
	)
	portofolio = forms.FileField(widget=CustomClearableFileInput(attrs={'placeholder':'PDF Maks 100 KB'}),
		label = "File Portofolio"
	)
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

class EvaluationForm(forms.ModelForm):
	management	= forms.IntegerField(min_value=0,max_value=100)
	creative	= forms.IntegerField(min_value=0,max_value=100)
	analisa		= forms.IntegerField(min_value=0,max_value=100)
	komunikasi	= forms.IntegerField(min_value=0,max_value=100)
	desain		= forms.IntegerField(min_value=0,max_value=100)
	logika		= forms.IntegerField(min_value=0,max_value=100)

	class Meta():
		model 	= Evaluation
		fields 	= ('management','creative','analisa','komunikasi','desain','logika',)