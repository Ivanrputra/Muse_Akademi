from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import FileInput
from django.contrib.auth import get_user_model
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _

from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from croppie.fields import CroppieField

from core.models import MentorData,Course,Session,Exam,SessionData,Order

# Form for user registration
class RegisterMentor(forms.ModelForm):
	class Meta():
		model 	= MentorData
		fields 	= ('status',)

class SessionDataForm(forms.ModelForm):
	class Meta():
		model 	= SessionData
		fields 	= ('title','attachment',)

class OrderForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['status'].choices    = Order.OrderStatusManagement.choices

	class Meta():
		model 	= Order
		fields 	= ('status',)
		
class SessionForm(forms.ModelForm):
	start_at = forms.DateTimeField(widget=DateTimePicker(
            options={
                # 'sideBySide':True,
                'useCurrent': True,
                'collapse': True,
                # 'inline': True,
                'keepOpen': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }),)

	def session_date_validation(form):
		course = form.instance.course
		if course.start_at > form.instance.start_at.date():
			form.add_error('start_at','Tgl mulai sesi tidak boleh sebelum dari tgl course dimulai : '+ str(course.start_at) +' s/d '+str(course.close_at)) 
		if course.close_at < form.instance.start_at.date():
			form.add_error('start_at','Tgl mulai sesi tidak boleh setelah dari tgl course ditutup : '+ str(course.start_at) +' s/d '+str(course.close_at)) 
		return form

	def __init__(self, *args, **kwargs):
		super(SessionForm, self).__init__(*args, **kwargs)
		self.fields['mentor'].queryset    = get_user_model().objects.filter(is_mentor=True)

	class Meta():
		model 	= Session
		fields 	= ('mentor','title','description','start_at',)

class ExamForm(forms.ModelForm):
	question    = forms.CharField(widget=SummernoteWidget())
	close_at	= forms.DateTimeField(widget=DateTimePicker(
            options={
                # 'sideBySide':True,
                'useCurrent': True,
                'collapse': True,
                # 'inline': True,
                'keepOpen': True,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }),)

	def exam_date_validation(form):
		course = form.instance.course
		if course.start_at > form.instance.close_at.date():
			form.add_error('close_at','Tgl mulai tugas tidak boleh sebelum dari tgl course dimulai : '+ str(course.start_at) +' s/d '+str(course.close_at)) 
		if course.close_at < form.instance.close_at.date():
			form.add_error('close_at','Tgl mulai tugas tidak boleh setelah dari tgl course ditutup : '+ str(course.start_at) +' s/d '+str(course.close_at)) 
		return form

	class Meta():
		model 	= Exam
		fields 	= ('question','close_at',)

class CourseForm(forms.ModelForm):
	start_at = close_at = forms.DateField(widget=DatePicker(
		options={
			'useCurrent': True,
			'collapse': True,
			'keepOpen': True,
		},
		attrs={
			'append': 'fa fa-calendar',
			'icon_toggle': True,
		}
	),)
	course_pic = CroppieField(
		options={
            'viewport': {
                'width': 240,
                'height': 140,
            },
            'boundary': {
                'width': 290,
                'height': 190,
            },
            'showZoomer': True,
        },
	)
	
	class Meta():
		model 	= Course
		fields 	= ('title','description','category','course_pic','price','start_at','close_at',)

class CourseUpdateForm(forms.ModelForm):
	start_at = close_at = forms.DateField(widget=DatePicker(
		options={
			'useCurrent': True,
			'collapse': True,
			'keepOpen': True,
		},
		attrs={
			'append': 'fa fa-calendar',
			'icon_toggle': True,
		}
	),)
	course_pic = CroppieField(
		options={
            'viewport': {
                'width': 240,
                'height': 140,
            },
            'boundary': {
                'width': 290,
                'height': 190,
            },
            'showZoomer': True,
        },
	)

	class Meta():
		model 	= Course
		fields 	= ('title','description','category','course_pic','price','start_at','close_at','is_publish')

