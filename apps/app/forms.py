from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import ExamProject,ExamAnswer,Order,Mitra

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

class MitraCreateForm(forms.ModelForm):
	# def clean_email(self):
		# username = self.cleaned_data.get('email')
		# if len(username.split(' ')) > 1:
		# 	raise forms.ValidationError(_('Username tidak boleh ada spasi')) 
		# if len(username) < 8:
		# 	raise forms.ValidationError(_('minimal karakter adalah 8')) 
		# user = get_user_model().objects.filter(username=username).exclude(pk=self.instance.id).exists()
		# if user:
		# 	raise forms.ValidationError('Username '+username+' tidak tersedia') 
		# return username

	class Meta():
		model 	= Mitra
		fields 	= ('email','phone','company_name','job_title','description')