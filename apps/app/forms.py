from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import ExamProject,ExamAnswer

# from core.models import EssayAnswer,CourseReview

# class CourseReviewForm(ModelForm):
#     comment     = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'form-control text-dark'}))
#     rating      = forms.FloatField(min_value=0,max_value=5,widget=forms.NumberInput(attrs={'class':'form-control text-dark','step': "0.1"}))
#     class Meta:
#         model = CourseReview
#         fields = ['rating','comment']

class ExamProjectForm(forms.ModelForm):
	class Meta():
		model 	= ExamProject
		fields 	= ('title','project',)

class ExamAnswerForm(forms.ModelForm):
	class Meta():
		model 	= ExamAnswer
		fields 	= ('answer',)
		