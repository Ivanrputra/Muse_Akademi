from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import ExamProject,ExamAnswer,Order

class ExamProjectForm(forms.ModelForm):
	class Meta():
		model 	= ExamProject
		fields 	= ('title','project',)

class ExamAnswerForm(forms.ModelForm):
	class Meta():
		model 	= ExamAnswer
		fields 	= ('answer',)
	
class OrderForm(forms.ModelForm):

	class Meta():
		model 	= Order
		fields 	= ('order_pic',)
		