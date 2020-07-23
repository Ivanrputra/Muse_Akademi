# Django Library
from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser, \
										BaseUserManager,PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files.uploadedfile import InMemoryUploadedFile

# Library
from PIL import Image as Img
from io import BytesIO
import sys

# module
from .models_settings import ProtectedFileSystemStorage, \
	ContentTypeRestrictedFileField,ContentTypeRestrictedFileFieldProtected, \
	get_course_pic_path,get_profile_path,get_cv_path,get_ktp_path, \
	get_npwp_path,get_certification_path,get_portofolio_path 

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
			image = Img.open(self.profile_pic)
			# image = Img.open(BytesIO(self.profile_pic.read()))
			image.thumbnail((100,100), Img.ANTIALIAS)
			output = BytesIO()
			if self.profile_pic.name.split('.')[-1] == 'png':
				image.save(output, format='PNG', quality=75)
				output.seek(0)
				self.profile_pic= InMemoryUploadedFile(output,'ImageField', "%s.png" %self.profile_pic.name, 'image/png', sys.getsizeof(output), None)
			else:
				image.save(output, format='JPEG', quality=75)
				output.seek(0)
				self.profile_pic= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.profile_pic.name, 'image/jpeg', sys.getsizeof(output), None)
		super(User, self).save(*args, **kwargs)

	objects		= UserManager()
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		db_table = 'user'

	def __str__(self):
		return self.firstname + ' ' + self.lastname

class MentorData(models.Model):
	admin			= models.ForeignKey(User,on_delete=models.CASCADE,related_query_name='admin',blank=True,null=True)
	mentor			= models.OneToOneField(User,on_delete=models.CASCADE,related_query_name='mentor',)
	cv				= ContentTypeRestrictedFileFieldProtected(upload_to=get_cv_path,						 max_upload_size=10485760)
	ktp				= ContentTypeRestrictedFileFieldProtected(upload_to=get_ktp_path,						 max_upload_size=10485760)
	npwp			= ContentTypeRestrictedFileFieldProtected(upload_to=get_npwp_path,default='',blank=True	,max_upload_size=10485760)
	certification	= ContentTypeRestrictedFileFieldProtected(upload_to=get_certification_path,				 max_upload_size=10485760)
	portofolio		= ContentTypeRestrictedFileFieldProtected(upload_to=get_portofolio_path,				 max_upload_size=10485760)

	created_at	= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at  = models.DateTimeField(auto_now=True)

	def __str__(self): 
		return str(self.mentor.email)
	
	class Meta:
		db_table = 'mentor_data'

class Category(models.Model):
	name 			= models.CharField(max_length=256)

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
	category		= models.ForeignKey(Category,on_delete=models.CASCADE)
	course_pic		= ContentTypeRestrictedFileField(
		content_types=['image/jpeg', 'image/png', 'image/bmp' ],max_upload_size=2097152,
		upload_to=get_course_pic_path
	)
	course_type 	= models.CharField(
		max_length=2,
		choices=CourseType.choices,
		default=CourseType.Short,
	)
	price			= models.IntegerField(validators=[MinValueValidator(0)])
	start_at		= models.DateField(auto_now=False, auto_now_add=False)
	close_at		= models.DateField(auto_now=False, auto_now_add=False)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if self.course_pic != None:
			image = Img.open(BytesIO(self.course_pic.read()))
			image.thumbnail((200,200), Img.ANTIALIAS)
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
		super(Course, self).save(*args, **kwargs)

	def is_free(self):
		if self.price == 0 : return True
		return False
		
	def __str__(self):
		return self.title

	class Meta:
		db_table = 'course'

class Session(models.Model):
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	mentor			= models.ManyToManyField(User)
	title 			= models.CharField(max_length=256,default='')
	description		= models.TextField()
	start_at		= models.DateTimeField(auto_now=False, auto_now_add=False)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'session'

class Library(models.Model):
	course			= models.ForeignKey(Course,on_delete=models.CASCADE)
	user			= models.ForeignKey(User,on_delete=models.CASCADE)

	created_at		= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'library'

class Review(models.Model):
	course		= models.ForeignKey(Course,on_delete=models.CASCADE)
	user		= models.ForeignKey(User,on_delete=models.CASCADE)
	rating		= models.FloatField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])
	comment		= models.TextField()

	created_at	= models.DateTimeField(auto_now=False, auto_now_add=True)
	updated_at	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.course.title

	class Meta:
		db_table = 'review'