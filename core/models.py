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
from django.db.models import Q
from django.core.mail import send_mail

# Library
import pytz
from PIL import Image as Img
from io import BytesIO
import sys
from datetime import timedelta
# import datetime
from crequest.middleware import CrequestMiddleware
# from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField

# module
from .models_utils import (ProtectedFileSystemStorage,get_category_image_path,
	ContentTypeRestrictedFileField,ContentTypeRestrictedFileFieldProtected,
	get_course_pic_path,get_profile_path,get_cv_path,get_ktp_path,
	get_npwp_path,get_certification_path,get_portofolio_path,
	get_session_attachment_path,get_order_attachment_path)


class ExamList:
	def __init__(self, exam,answer):
		self.exam		= exam
		self.answer		= answer
	
class ReportList:
	def __init__(self, exam,mentors_report):
		self.exam			= exam
		self.mentor_report	= mentors_report

class MentorReportList:
	def __init__(self, mentor,report):
		self.mentor	= mentor
		self.report	= report

class MentorEvaluationList:
	def __init__(self, mentor,evaluation):
		self.mentor		= mentor
		self.evaluation	= evaluation

class MyEvaluation:
	def __init__(self, management,creative,analisa,komunikasi,desain,logika):
		self.management	= management
		self.creative	= creative
		self.analisa	= analisa
		self.komunikasi	= komunikasi
		self.desain		= desain
		self.logika		= logika

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
	# is_partner	= models.BooleanField(default=False)

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

	@property
	def is_have_mitra(self):
		if MitraUser.objects.filter(user=self.pk).count() > 0:
			return True
		return False

	def orders(self):
		return Order.objects.filter(user=self.id)

	def evaluations(self):
		e = Evaluation.objects.filter(library__user=self.id).aggregate(
			Avg('management'),Avg('creative'),Avg('analisa'),Avg('komunikasi'),Avg('desain'),Avg('logika'))
		return MyEvaluation(e['management__avg'],e['creative__avg'],e['analisa__avg'],e['komunikasi__avg'],e['desain__avg'],e['logika__avg'])
		
	def courses(self):
		return Course.objects.filter(library__user=self.id)

	def libraries(self):
		return Library.objects.filter(user=self.id)
	
	def session_active(self):
		return Session.objects.filter(course__library__user=self.id,start_at__gte=timezone.now())
	
	def mentor_courses(self):
		if self.is_mentor:
			return Course.objects.filter(session__mentor=self.id,is_publish=True).distinct()
		return 0
	
	def mentor_session_active(self):
		if self.is_mentor:
			return Session.objects.filter(mentor=self.id,start_at__gte=timezone.now(),course__is_publish=True)
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

	def management_session_active(self):
		if self.is_staff:
			return Session.objects.filter(course__admin=self.id,start_at__gte=timezone.now(),course__is_publish=True)
		return 0
	
	def management_mentors(self):
		if self.is_staff:
			return MentorData.objects.all()
			# return MentorData.objects.all().exclude(mentor=self.id,mentor__is_mentor=False)
		return 0

	def mentor_data(self):
		return MentorData.objects.filter(mentor=self.id).first()

	def mitra_course_available(self):
		return Course.objects.filter(is_publish=True,mitra__mitrauser__user=self.id).exclude(library__user=self.id)

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""
		Send an email to this user.
		"""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	class Meta:
		db_table = 'user'
		ordering = ['email']

class Institution(models.Model):
	title	= models.CharField(max_length=50)

	def __str__(self): 
		return str(self.title)
	
	class Meta:
		db_table = 'intitution'
		ordering = ['title']


class MentorData(models.Model):
	class MentorStatus(models.TextChoices):
		accepted	= 'AC', _('Diterima')	#Accepted
		waiting		= 'WA', _('Menunggu Konfirmasi')	#Waiting
		decline		= 'DE', _('TIdak Valid')	#Decline

	admin			= models.ForeignKey(User,on_delete=models.CASCADE,related_query_name='admin',blank=True,null=True)
	mentor			= models.OneToOneField(User,on_delete=models.CASCADE,related_query_name='mentor',)
	no_ktp			= models.CharField(max_length=20)
	cv				= ContentTypeRestrictedFileFieldProtected(upload_to=get_cv_path,						 max_upload_size=2621440)
	ktp				= ContentTypeRestrictedFileFieldProtected(upload_to=get_ktp_path,						 max_upload_size=2621440)
	npwp			= ContentTypeRestrictedFileFieldProtected(upload_to=get_npwp_path,null=True,default='',blank=True, max_upload_size=2621440)
	certification	= ContentTypeRestrictedFileFieldProtected(upload_to=get_certification_path,				 max_upload_size=2621440)
	portofolio		= ContentTypeRestrictedFileFieldProtected(upload_to=get_portofolio_path,				 max_upload_size=2621440)
	
	headline		= models.CharField(null=True,blank=True,max_length=255)
	biography		= models.TextField(null=True,blank=True)

	status 			= models.CharField(
		max_length=2,
		choices=MentorStatus.choices,
		default=MentorStatus.waiting,
	)
	institution		= models.ForeignKey(Institution,on_delete=models.PROTECT,null=True,blank=True,)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at  	= models.DateTimeField(auto_now=True)

	@property
	def is_partner(self):
		if self.institution: return True
		return False
		 
	def __str__(self): 
		return str(self.mentor.email)
	
	class Meta:
		db_table = 'mentor_data'
		ordering = ['mentor']

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
 
class Mitra(models.Model):
	class MitraStatus(models.TextChoices):
		waiting_confirmation 	= 'WC', _('Menunggu Konfirmasi')
		confirmed 				= 'CO', _('Selesai')
		decline 				= 'DE', _('TIdak Valid')
		
	title			= models.CharField(max_length=256)
	email			= models.EmailField(max_length=50)
	user_admin		= models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_mitra')
	max_user		= models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0)])
	phone			= PhoneNumberField(max_length=15)
	company_name	= models.CharField(max_length=256)
	job_title		= models.CharField(max_length=256)
	description		= models.TextField()
	status 			= models.CharField(
		max_length=2,
		choices=MitraStatus.choices,
		default=MitraStatus.waiting_confirmation,
	)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f'{self.company_name}'

	@property
	def is_valid(self):
		if self.status != "CO":
			return False
		return True

	def get_course_list(self):
		return Course.objects.filter(mitra=self.pk,is_publish=True)
	
	def get_user_list(self):
		return MitraUser.objects.filter(mitra=self.pk)
	
	def get_invited_user_list(self):
		return MitraInvitedUser.objects.filter(mitra=self.pk)
	
	def get_pending_user_list(self):
		return MitraInvitedUser.objects.filter(mitra=self.pk,is_confirmed=False)

	class Meta:
		ordering	= ['status','updated_at']
		db_table 	= 'mitra'

class MitraUser(models.Model):
	user			= models.ForeignKey(User,on_delete=models.CASCADE)
	is_admin		= models.BooleanField(default=False)
	is_co_host		= models.BooleanField(default=False)
	mitra			= models.ForeignKey(Mitra,on_delete=models.CASCADE)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'mitra_user'

class MitraInvitedUser(models.Model):
	email			= models.EmailField()
	mitra			= models.ForeignKey(Mitra,on_delete=models.CASCADE)
	is_confirmed	= models.BooleanField(default=False)
	invited_by		= models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		unique_together = (('email', 'mitra'),)
		db_table = 'mitra_invited_user'

class Course(models.Model):
	class CourseTypeChoice(models.TextChoices):
		all_user 				= 'AU', _('Semua user') # user.all() > course > price
		mitra_only				= 'MO',	_('Hanya untuk invited_user') # course.invited_user.all() > course.get_price
		all_user_n_mitra_free	= 'MF', _('Untuk semua user, tapi invited_user gratis') # user.all() > course.get_price && (course.invited_user.all() > Free)


	admin			= models.ForeignKey(User,on_delete=models.CASCADE)
	title 			= models.CharField(max_length=256,default='')
	description		= models.TextField()
	category		= models.ManyToManyField(Category)
	course_pic		= ContentTypeRestrictedFileField(
		content_types=['image/jpeg', 'image/png', 'image/bmp' ],max_upload_size=2097152,
		upload_to=get_course_pic_path
	)
	url_meet		= models.URLField()
	price			= models.IntegerField(validators=[MinValueValidator(0)])
	discount		= models.IntegerField(null=True,blank=True,validators=[MinValueValidator(1),MaxValueValidator(100)])
	start_at		= models.DateField(auto_now=False, auto_now_add=False)
	close_at		= models.DateField(auto_now=False, auto_now_add=False)

	mitra 			= models.ForeignKey(Mitra,on_delete=models.CASCADE,null=True,blank=True)

	is_publish		= models.BooleanField(default=False)

	# invited_user	= models.ManyToManyField(User,related_name='invited_user')
	# link_invitation	= models.URLField(null=True,blank=True)
	# course_type		= models.CharField(
	# 	max_length=2,
	# 	choices=CourseTypeChoice.choices,
	# 	default=CourseTypeChoice.all_user,
	# )

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

	def get_price(self):
		if self.price > 0:
			if self.discount:
				return int(self.price - (self.discount / 100 * self.price))
		return self.price

	def get_progress(self):
		now = timezone.now()
		# print(int((self.sessions().filter(start_at__lte=now).count() / (self.sessions().count() or 1) * 100)))
		return int((self.sessions().filter(start_at__lte=now).count() / (self.sessions().count() or 1) * 100))

	def status(self):
		now = timezone.now().date()
		if now < self.start_at: return 'Not Active'
		elif now >= self.start_at and self.close_at >= now: return 'Active'
		elif now > self.close_at: return 'Done'
	
	@property
	def is_partner(self):
		if User.objects.filter(session__course=self.id,mentor__institution__isnull=False).count() > 0:
			return True
		return False
	
	@property
	def is_mitra(self):
		if self.mitra: return True
		return False

	def is_close(self):
		
		date_range = self.close_at - timezone.now().date()
		if date_range < timedelta(days=0):
			return True
		return False
		
	def is_have(self):
		try: 
			current_request = CrequestMiddleware.get_request()
			return Library.objects.filter(course=self.id,user=current_request.user).exists()
		except : return False

	def type_str(self):
		if self.close_at-self.start_at <= timedelta(days=30):
			return "Kursus Pendek"
		return "Kursus Panjang"

	def is_free(self):
		if self.get_price() == 0 : return True
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

	def relevant_courses(self):
		return Course.objects.filter(category__in=self.category.all(),is_publish=True)[:8]

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
	
	def is_open_now(self):
		date_range = self.start_at - timezone.now()
		if date_range < timedelta(hours=-6):
			return "No"
		elif date_range > timedelta(days=1,hours=0):
			return "Not Yet"
		return "Yes"
		# if self.start_at.date() != timezone.now().date():
		# 	return False
		# return True

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'session'
		ordering = ['start_at']

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

		# exam_list		= Exam.objects.filter(course=self.exam.course)
		# examanswer_list	= ExamAnswer.objects.filter(exam__in=exam_list,user=self.user,summary__isnull=False)
		# if exam_list.count() == examanswer_list.count():
		# 	library = get_object_or_404(Library,user=self.user,course=self.exam.course)
		# 	library.summary = examanswer_list.aggregate(Avg('summary'))['summary__avg']
		# 	library.save()

	def projects(self):
		return ExamProject.objects.filter(exam_answer=self.id)
	
	# def mentor_report(self):
	# 	mentors_report = []
	# 	for mentor in User.objects.filter(session__course=self.exam.course).distinct():
	# 		mentors_report.append(
	# 			MentorReportList(mentor,ExamReport.objects.filter(mentor=mentor,exam_answer=self.id).first())
	# 		)
	# 	return mentors_report

	class Meta:
		db_table = 'exam_answer'

class ExamProject(models.Model):
	exam_answer		= models.ForeignKey(ExamAnswer,on_delete=models.CASCADE)
	title			= models.CharField(max_length=256)
	url_project		= models.URLField()
	# ContentTypeRestrictedFileFieldProtected(upload_to=get_project_path,max_upload_size=10485760)
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
	is_private		= models.BooleanField(default=False) 
	summary			= models.DecimalField(null=True,blank=True,max_digits=5, decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)])

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	
	def user_exam_answer(self):
		return ExamAnswer.objects.filter(user=self.user,exam__in=Exam.objects.filter(course=self.course))

	def exams(self):
		# exam_answer 	= ExamAnswer.objects.filter(exam=OuterRef('pk'),user=self.user).values('answer')
		# return Exam.objects.annotate(answer=Subquery(exam_answer)).filter(course=self.course)
		exams = []
		for exam in Exam.objects.filter(course=self.course):
			exams.append(ExamList(
				exam,
				ExamAnswer.objects.filter(exam=exam,user=self.user).first(),
			))
		return exams

	def mentor_evaluation(self):
		mentors_evaluations = []
		for mentor in User.objects.filter(session__course=self.course).distinct():
			mentors_evaluations.append(
				MentorEvaluationList(mentor,Evaluation.objects.filter(mentor=mentor,library=self.id).first())
			)
		return mentors_evaluations
	

	def __str__(self):
		return f'{self.user} -> {self.course} -> summary : {self.summary}'

	class Meta:
		db_table = 'library'

class Evaluation(models.Model):
	library		= models.ForeignKey(Library,on_delete=models.CASCADE)
	mentor		= models.ForeignKey(User,on_delete=models.CASCADE)
	
	management	= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	creative	= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	analisa		= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	komunikasi	= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	desain		= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 
	logika		= models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 

	summary		= models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(0),MaxValueValidator(100)])
	
	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.summary = (self.management + self.creative + self.analisa + self.komunikasi + self.desain + self.logika) / 6
		super(Evaluation, self).save(*args, **kwargs)

		mentor_list			= User.objects.filter(session__course=self.library.course).distinct()
		mentor_evaluation 	= Evaluation.objects.filter(library=self.library,mentor__in=mentor_list)
		if mentor_list.count() == mentor_evaluation.count():
			self.library.summary = mentor_evaluation.aggregate(Avg('summary'))['summary__avg']
			self.library.save()

	class Meta:
		db_table = 'evaluation'

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

	class OrderStatusUser(models.TextChoices):
		waiting_payment 		= 'WP', _('Menunggu Pembayaran') # Waiting for Payment
	
	class OrderStatusManagement(models.TextChoices):
		waiting_confirmation 	= 'WC', _('Menunggu Konfirmasi') # Waiting for Confirmation
		confirmed 				= 'CO', _('Selesai')
		decline 				= 'DE', _('TIdak Valid')
		
	# invoice_no 	= models.CharField(max_length = 500, default = increment_invoice_number, null = True, blank = True)
	invoice_no 		= models.CharField(max_length=500,null=True,blank=True)
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	price			= models.IntegerField()
	discount		= models.IntegerField(null=True,blank=True,validators=[MinValueValidator(1),MaxValueValidator(100)])
	user			= models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
	admin			= models.ForeignKey(User,on_delete=models.CASCADE,related_query_name='admin',null=True,blank=True)
	order_pic		= ContentTypeRestrictedFileFieldProtected(null=True,blank=True,content_types=['image/jpeg', 'image/png', 'image/bmp' ],upload_to=get_order_attachment_path,max_upload_size=5242880)
	status 			= models.CharField(
		max_length=2,
		choices=OrderStatusUser.choices+OrderStatusManagement.choices,
		default=OrderStatusUser.waiting_payment,
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
		super(Order, self).save(*args, **kwargs)

	def get_price(self):
		if self.price > 0:
			if self.discount:
				return int(self.price - (self.discount / 100 * self.price))
		return self.price

	def __str__(self):
		return f'{self.user}'

	class Meta:
		db_table = 'order'
		ordering = ['created_at']

class Schedule(models.Model):
	class Day(models.TextChoices):
		sunday		= 'SUN', _('Sunday')
		monday		= 'MON', _('Monday')
		tuesday		= 'TUE', _('Tuesday')
		wednesday	= 'WED', _('Wednesday')
		thursday	= 'THU', _('Thursday')
		friday		= 'FRI', _('Friday')
		saturday	= 'SAT', _('Saturday')

	mentor	= models.ForeignKey(User,on_delete=models.CASCADE)
	day 	= models.CharField(
		max_length=3,
		choices=Day.choices,
		# default=Day.Short,
	)
	time	= models.TimeField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return self.mentor.username

	class Meta:
		db_table = 'schedule'