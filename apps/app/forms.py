from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import ExamProject,ExamAnswer,Order

class ExamProjectForm(forms.ModelForm):
	title   	= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Judul Tugas'}))
	url_project = forms.CharField(widget=forms.URLInput(attrs={'class':'form-control','placeholder':'URL File Pengumpulan Tugas'}))
	class Meta():
		model 	= ExamProject
		fields 	= ('title','url_project',)

class ExamAnswerForm(forms.ModelForm):
	answer		= forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':'5','placeholder':'Deskripsikan tentang tugas yang Anda buat secara singkat...'}))
	class Meta():
		model 	= ExamAnswer
		fields 	= ('answer',)
	
class OrderForm(forms.ModelForm):

	class Meta():
		model 	= Order
		fields 	= ('order_pic',)
		