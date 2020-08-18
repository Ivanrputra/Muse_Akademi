# Django Library
from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser, \
										BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from django.db.models import Count,Avg,OuterRef, Subquery
from django.shortcuts import render,get_object_or_404

# Library
import pytz
from PIL import Image as Img
from io import BytesIO
import sys
# import datetime
from crequest.middleware import CrequestMiddleware
# from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField

# module
from .models_utils import (ProtectedFileSystemStorage,get_category_image_path,
	ContentTypeRestrictedFileField,ContentTypeRestrictedFileFieldProtected,
	get_course_pic_path,get_profile_path,get_cv_path,get_ktp_path,
	get_npwp_path,get_certification_path,get_portofolio_path,get_project_path,
	get_session_attachment_path,get_order_attachment_path)


class ExamList:
	def __init__(self, exam,answer):
		self.question	= exam
		self.answer		= answer
	
class ReportList:
	def __init__(self, exam,mentors_report):
		self.exam			= exam
		self.mentor_report	= mentors_report

class MentorReportList:
	def __init__(self, mentor,report):
		self.mentor	= mentor
		self.report	= report

# Create your models here.

# -------------------------------------------USER-------------------------------------------
# Managing custom create user and and superuser using BaseUserManager.
class UserManager(BaseUserManager):
	def create_user(self,email,password=None,**extra_fields):
		# create and save a new user
		if not email:
			raise ValueError("User must have an email address")
		
		user = User.objects.filter(email=self.normalize_email(email))
		if user.count() == 0:
			user 	= self.model(email=self.normalize_email(email),**extra_fields)
			
			user.set_password(password)
			user.save(using=self._db)
			return user

		return user.first()

	def create_superuser(self,email,username,password):
		# create and save a new superuser
		user 					= self.create_user(email,password)
		user.username			= username
		user.is_staff 			= True
		user.is_superuser		= True
		user.is_active			= True
		user.is_mentor			= True
		user.is_user			= True
		user.save(using=self._db)

		return user

# Custom user model using
class User(AbstractBaseUser,PermissionsMixin):
	# Custom user model that support using email instead username
	firstname	= models.CharField(max_length=256)
	lastname	= models.CharField(max_length=256)
	email		= models.EmailField(max_length=50,unique=True)
	username	= models.CharField(max_length=256,unique=True)
	phone		= PhoneNumberField(max_length=15)
	address		= models.TextField(null=True,blank=True)
	password	= models.CharField(max_length=256)
	profile_pic = ContentTypeRestrictedFileField(
        content_types=['image/jpeg', 'image/png', 'image/bmp' ],max_upload_size=2097152,
        upload_to=get_profile_path,null=True,blank=True
    )

	is_active	= models.BooleanField(default=True) 
	is_user		= models.BooleanField(default=True) 
	is_staff	= models.BooleanField(default=False) 
	is_mentor	= models.BooleanField(default=False)

	created_at	= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at  = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if self.profile_pic:
			try:
				image = Img.open(self.profile_pic)
				# image = Img.open(BytesIO(self.profile_pic.read()))
				image.thumbnail((150,150), Img.ANTIALIAS)
				output = BytesIO()
				if self.profile_pic.name.split('.')[-1] == 'png':
					image.save(output, format='PNG', quality=100)
					output.seek(0)
					self.profile_pic= InMemoryUploadedFile(output,'ImageField', "%s.png" %self.profile_pic.name, 'image/png', sys.getsizeof(output), None)
				else:
					image.save(output, format='JPEG', quality=100)
					output.seek(0)
					self.profile_pic= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.profile_pic.name, 'image/jpeg', sys.getsizeof(output), None)
			except:
				pass
		super(User, self).save(*args, **kwargs)

	objects		= UserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.firstname +' '+ self.lastname

	def orders(self):
		return Order.objects.filter(user=self.id)

	def courses(self):
		return Course.objects.filter(library__user=self.id)
	
	def course_active(self):
		return Course.objects.filter(library__user=self.id,start_at__lte=timezone.now().date(),close_at__gte=timezone.now().date())
	
	def course_not_active(self):
		return Course.objects.filter(library__user=self.id,close_at__lt=timezone.now().date())

	def libraries(self):
		return Library.objects.filter(user=self.id)
	
	def schedules(self):
		return Session.objects.filter(course__library__user=self.id,start_at__gte=timezone.now())
	
	def mentor_courses(self):
		if self.is_mentor:
			return Course.objects.filter(session__mentor=self.id,is_publish=True).distinct()
		return 0
	
	def mentor_courses_active(self):
		if self.is_mentor:
			return Course.objects.filter(session__mentor=self.id,start_at__lte=timezone.now().date(),close_at__gte=timezone.now().date(),is_publish=True,).distinct()
		return 0
	
	def mentor_courses_not_active(self):
		if self.is_mentor:
			return Course.objects.filter(session__mentor=self.id,close_at__lt=timezone.now().date(),is_publish=True,).distinct()
		return 0

	def mentor_schedules(self):
		if self.is_mentor:
			return Session.objects.filter(mentor=self.id,start_at__gte=timezone.now())
		return 0
	
	def schedule(self):
		if self.is_mentor:
			# days = ['SU','MO','TU','WE','TH','FR','SA']
			# ordering = "FIELD('day', %s)" % ",".join(str(id) for id in days)
			# 'SU','MO','TU','WE','TH','FR','SA'
			return Schedule.objects.filter(mentor=self.id).extra(
           		select={'ordering': 'FIELD(day, "SU","MO","TU","WE","TH","FR","SA")'}, order_by=('ordering',))
			# .extra(
			# 	select={'days': "FIELD(day, 'SU','MO','TU','WE','TH','FR','SA')"},
			# 	order_by=['days']
			# )
		return 0
	
	def management_courses(self):
		if self.is_staff:
			return Course.objects.filter(admin=self.id)
		return 0
	
	def management_schedules(self):
		if self.is_staff:
			return Session.objects.filter(course__admin=self.id,start_at__gte=timezone.now())
		return 0
	
	class Meta:
		db_table = 'user'

	def mentor_data(self):
		return MentorData.objects.filter(mentor=self.id).first()

class MentorData(models.Model):
	class MentorStatus(models.TextChoices):
		accepted	= 'AC', _('Accepted')
		waiting		= 'WA', _('Waiting')
		decline		= 'DE', _('Decline')

	admin			= models.ForeignKey(User,on_delete=models.CASCADE,related_query_name='admin',blank=True,null=True)
	mentor			= models.OneToOneField(User,on_delete=models.CASCADE,related_query_name='mentor',)
	no_ktp			= models.CharField(max_length=20)
	cv				= ContentTypeRestrictedFileFieldProtected(upload_to=get_cv_path,						 max_upload_size=10485760)
	ktp				= ContentTypeRestrictedFileFieldProtected(upload_to=get_ktp_path,						 max_upload_size=10485760)
	npwp			= ContentTypeRestrictedFileFieldProtected(upload_to=get_npwp_path,null=True,default='',blank=True, max_upload_size=10485760)
	certification	= ContentTypeRestrictedFileFieldProtected(upload_to=get_certification_path,				 max_upload_size=10485760)
	portofolio		= ContentTypeRestrictedFileFieldProtected(upload_to=get_portofolio_path,				 max_upload_size=10485760)

	status 			= models.CharField(
		max_length=2,
		choices=MentorStatus.choices,
		default=MentorStatus.waiting,
	)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at  	= models.DateTimeField(auto_now=True)

	def __str__(self): 
		return str(self.mentor.email)
	
	class Meta:
		db_table = 'mentor_data'

class Category(models.Model):
	category_pic	= ContentTypeRestrictedFileField(upload_to=get_category_image_path,max_upload_size=2097152,null=True,default='',blank=True,)
	name 			= models.CharField(max_length=256)

	def save(self, *args, **kwargs):
		if self.category_pic:
			image = Img.open(self.category_pic)
			image.thumbnail((40,40), Img.ANTIALIAS)
			output = BytesIO()
			if self.category_pic.name.split('.')[-1] == 'png':
				image.save(output, format='PNG', quality=75)
				output.seek(0)
				self.category_pic = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.category_pic.name, 'image/png', sys.getsizeof(output), None)
			else:
				image.save(output, format='JPEG', quality=75)
				output.seek(0)
				self.category_pic = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.category_pic.name, 'image/jpeg', sys.getsizeof(output), None)
		super(Category, self).save(*args, **kwargs)

	def __str__(self): 
		return self.name
	
	class Meta:
		db_table = 'category'

class Course(models.Model):
	class CourseType(models.TextChoices):
		Short 	= 'SH', _('Short')
		Long 	= 'LO', _('Long')

	admin			= models.ForeignKey(User,on_delete=models.CASCADE)
	title 			= models.CharField(max_length=256,default='')
	description		= models.TextField()
	category		= models.ManyToManyField(Category)
	course_pic		= ContentTypeRestrictedFileField(
		content_types=['image/jpeg', 'image/png', 'image/bmp' ],max_upload_size=2097152,
		upload_to=get_course_pic_path
	)
	# course_type 	= models.CharField(
	# 	max_length=2,
	# 	choices=CourseType.choices,
	# 	default=CourseType.Short,
	# )
	price			= models.IntegerField(validators=[MinValueValidator(0)])
	start_at		= models.DateField(auto_now=False, auto_now_add=False)
	close_at		= models.DateField(auto_now=False, auto_now_add=False)

	is_publish		= models.BooleanField(default=False)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if self.course_pic:
			try:
				image = Img.open(self.course_pic)
				# image = Img.open(BytesIO(self.course_pic.read()))
				image.thumbnail((300,175), Img.ANTIALIAS)
				output = BytesIO()
				# course_pic
				if self.course_pic.name.split('.')[-1] == 'png':
					image.save(output, format='PNG', quality=75)
					output.seek(0)
					self.course_pic= InMemoryUploadedFile(output,'ImageField', "%s.png" %self.course_pic.name, 'image/png', sys.getsizeof(output), None)
				else:
					image.save(output, format='JPEG', quality=75)
					output.seek(0)
					self.course_pic= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.course_pic.name, 'image/jpeg', sys.getsizeof(output), None)			
			except:
				pass
		super(Course, self).save(*args, **kwargs)

	def course_type(self):
		if Session.objects.filter(course=self.id).count() < 2:
			return "Short"
		return "Long"

	def is_free(self):
		if self.price == 0 : return True
		return False
	
	def mentors(self):
		return User.objects.filter(session__course=self.id).distinct()

	def libraries(self):
		return Library.objects.filter(course=self.id)

	def students(self):
		return User.objects.filter(library__course=self.id)

	def sessions(self):
		return Session.objects.filter(course=self.id)

	def exams(self):
		return Exam.objects.filter(course=self.id)

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'course'
		ordering = ['start_at']

class Session(models.Model):
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	mentor			= models.ManyToManyField(User)
	title 			= models.CharField(max_length=256,default='')
	description		= models.TextField()
	start_at		= models.DateTimeField(auto_now=False, auto_now_add=False)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def session_datas(self):
		return SessionData.objects.filter(session=self.id)

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'session'

class SessionData(models.Model):
	session			= models.ForeignKey(Session,on_delete=models.CASCADE)
	title			= models.CharField(max_length=256)
	attachment		= ContentTypeRestrictedFileFieldProtected(upload_to=get_session_attachment_path,max_upload_size=10485760)
	
	def __str__(self):
		return self.title

	class Meta:
		db_table = 'session_data'

class Exam(models.Model):
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	question		= models.TextField()
	close_at		= models.DateTimeField(auto_now=False, auto_now_add=False)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def user_answer(self):
		try: 
			current_request = CrequestMiddleware.get_request()
			return ExamAnswer.objects.filter(exam=self.id,user=current_request.user).first()
		except : return None
	
	class Meta:
		db_table = 'exam'
		ordering = ['close_at']

class ExamAnswer(models.Model):
	exam			= models.ForeignKey(Exam,on_delete=models.CASCADE)
	user			= models.ForeignKey(User,on_delete=models.CASCADE)
	answer			= models.TextField(default='')
	summary			= models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)])

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		super(ExamAnswer, self).save(*args, **kwargs)

		exam_list		= Exam.objects.filter(course=self.exam.course)
		examanswer_list	= ExamAnswer.objects.filter(exam__in=exam_list,user=self.user,summary__isnull=False)
		if exam_list.count() == examanswer_list.count():
			library = get_object_or_404(Library,user=self.user,course=self.exam.course)
			library.summary = examanswer_list.aggregate(Avg('summary'))['summary__avg']
			library.save()

	def projects(self):
		return ExamProject.objects.filter(exam_answer=self.id)
	
	def mentor_report(self):
		mentors_report = []
		for mentor in User.objects.filter(session__course=self.exam.course).distinct():
			mentors_report.append(
				MentorReportList(mentor,ExamReport.objects.filter(mentor=mentor,exam_answer=self.id).first())
			)
		return mentors_report

	class Meta:
		db_table = 'exam_answer'

class ExamProject(models.Model):
	exam_answer		= models.ForeignKey(ExamAnswer,on_delete=models.CASCADE)
	title			= models.CharField(max_length=256)
	project			= ContentTypeRestrictedFileFieldProtected(upload_to=get_project_path,max_upload_size=10485760)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'exam_project'

class ExamReport(models.Model):
	# exam			= models.ForeignKey(Exam,on_delete=models.CASCADE)
	# user			= models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
	exam_answer		= models.ForeignKey(ExamAnswer,on_delete=models.CASCADE)
	mentor			= models.ForeignKey(User,on_delete=models.CASCADE)
	
	ide				= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	konsep			= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	desain			= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	proses			= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	produk			= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
	summary			= models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)])
	
	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.summary = (self.ide + self.konsep + self.desain + self.proses + self.produk) / 5
		super(ExamReport, self).save(*args, **kwargs)

		mentor_list		= User.objects.filter(session__course=self.exam_answer.exam.course).distinct()
		mentor_menilai 	= ExamReport.objects.filter(exam_answer=self.exam_answer,mentor__in=mentor_list)
		if mentor_list.count() == mentor_menilai.count():
			self.exam_answer.summary = mentor_menilai.aggregate(Avg('summary'))['summary__avg']
			self.exam_answer.save()

	class Meta:
		db_table = 'exam_report'

class Library(models.Model):
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	user			= models.ForeignKey(User,on_delete=models.CASCADE)
	summary			= models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)])

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	
	def exam_anwers(self):
		return ExamAnswer.objects.filter(exam__course=self.course,user=self.user)
	
	def exams(self):
		# exam_answer 	= ExamAnswer.objects.filter(exam=OuterRef('pk'),user=self.user).values('answer')
		# return Exam.objects.annotate(answer=Subquery(exam_answer)).filter(course=self.course)
		exa = []
		for exam in Exam.objects.filter(course=self.course):
			exa.append(ExamList(
				exam.question,
				ExamAnswer.objects.filter(exam=exam,user=self.user).first(),
			))
		return exa

	class Meta:
		db_table = 'library'

def increment_invoice_number():
	last_invoice = Order.objects.all().order_by('id').last()
	if not last_invoice:
		return 'MAG000001'
	invoice_no = last_invoice.invoice_no
	# if not last_invoice.invoice_no:
	# 	return 'MNO000001'
	invoice_int = int(invoice_no.split('MAG')[-1])
	width = 6
	new_invoice_int = invoice_int + 1
	formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
	new_invoice_no = 'MAG' + str(formatted)
	return new_invoice_no 

# class Order(models.Model):

# 	class OrderStatus(models.TextChoices):
# 		order_created 			= 'OC', _('Order Created')
# 		waiting_payment 		= 'WP', _('Waiting for Payment')
# 		# waiting_confirmation 	= 'WC', _('Waiting for Confirmation')
# 		confirmed 				= 'CO', _('Confirmed')
# 		# cancel / expire / deny
# 		canceled 				= 'CA', _('Canceled')
# 		refund 					= 'RE', _('Refund')
# 		fraud_challenge 		= 'FC', _('Fraud Challenge')
# 	# invoice_no 	= models.CharField(max_length = 500, default = increment_invoice_number, null = True, blank = True)
# 	invoice_no 	= models.CharField(max_length = 500,  null = True, blank = True)
# 	course		= models.ForeignKey(Course,on_delete=models.CASCADE)
# 	price		= models.IntegerField()
# 	user		= models.ForeignKey(User,on_delete=models.CASCADE)
# 	transaction_url	= models.CharField(max_length = 500,  null = True, blank = True)
# 	status 		= models.CharField(
# 		max_length=2,
# 		choices=OrderStatus.choices,
# 		default=OrderStatus.order_created,
# 	)
	
# 	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
# 	updated_at		= models.DateTimeField(auto_now=True)

# 	class Meta:
# 		db_table = 'order'

class Order(models.Model):

	class OrderStatus(models.TextChoices):
		order_created 			= 'OC', _('Order Created')
		waiting_payment 		= 'WP', _('Waiting for Payment')
		# waiting_confirmation 	= 'WC', _('Waiting for Confirmation')
		confirmed 				= 'CO', _('Confirmed')
		# cancel / expire / deny
		canceled 				= 'CA', _('Canceled')
		refund 					= 'RE', _('Refund')
		fraud_challenge 		= 'FC', _('Fraud Challenge')
	# invoice_no 	= models.CharField(max_length = 500, default = increment_invoice_number, null = True, blank = True)
	invoice_no 		= models.CharField(max_length = 500,  null = True, blank = True)
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	price			= models.IntegerField()
	user			= models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
	admin			= models.ForeignKey(User,on_delete=models.CASCADE,related_query_name='admin')
	order_pic		= ContentTypeRestrictedFileFieldProtected(null=True,blank=True,upload_to=get_order_attachment_path,max_upload_size=5242880)
	status 			= models.CharField(
		max_length=2,
		choices=OrderStatus.choices,
		default=OrderStatus.order_created,
	)
	
	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if self.order_pic:
			try:
				image = Img.open(self.order_pic)
				image.thumbnail((350,600), Img.ANTIALIAS)
				output = BytesIO()
				if self.order_pic.name.split('.')[-1] == 'png':
					image.save(output, format='PNG', quality=75)
					output.seek(0)
					self.order_pic= InMemoryUploadedFile(output,'ImageField', "%s.png" %self.order_pic.name, 'image/png', sys.getsizeof(output), None)
				else:
					image.save(output, format='JPEG', quality=75)
					output.seek(0)
					self.order_pic= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.order_pic.name, 'image/jpeg', sys.getsizeof(output), None)			
			except:
				pass
		super(Course, self).save(*args, **kwargs)

	class Meta:
		db_table = 'order'

class Schedule(models.Model):
	class Day(models.TextChoices):
		sunday		= 'SU', _('Sunday')
		monday		= 'MO', _('Monday')
		tuesday		= 'TU', _('Tuesday')
		wednesday	= 'WE', _('Wednesday')
		thursday	= 'TH', _('Thursday')
		friday		= 'FR', _('Friday')
		saturday	= 'SA', _('Saturday')

	mentor	= models.ForeignKey(User,on_delete=models.CASCADE)
	day 	= models.CharField(
		max_length=2,
		choices=Day.choices,
		# default=Day.Short,
	)
	time	= models.TimeField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return self.mentor.username

	class Meta:
		db_table = 'schedule'