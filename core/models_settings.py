from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser, \
										BaseUserManager,PermissionsMixin

from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.utils.functional import cached_property

from django.conf import settings

class ProtectedFileSystemStorage(FileSystemStorage):
	"""
	A class to manage protected files.
	We have to override the methods in the FileSystemStorage class which
	are decorated with cached_property for this class to work as intended.
	"""
	def __init__(self, *args, **kwargs):
		kwargs["location"] = settings.PROTECTED_MEDIA_ROOT
		kwargs["base_url"] = settings.PROTECTED_MEDIA_URL
		super(ProtectedFileSystemStorage, self).__init__(*args, **kwargs)

class ContentTypeRestrictedFileField(models.FileField):
	"""
	Same as FileField, but you can specify:
	\t* content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
	\t* max_upload_size - a number indicating the maximum file size allowed for upload.
	\t\t2.5MB - 2621440
	\t\t5MB - 5242880
	\t\t10MB - 10485760
	\t\t20MB - 20971520
	\t\t50MB - 5242880
	\t\t100MB - 104857600
	\t\t250MB - 214958080
	\t\t500MB - 429916160
	"""
	def __init__(self, *args, **kwargs):
		self.content_types = kwargs.pop("content_types", [])
		self.max_upload_size = kwargs.pop("max_upload_size", [])
		super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
		file = data.file
		try:
			content_type = file.content_type
			
			if content_type in self.content_types or self.content_types == []:
				if file.size:
					if file.size > self.max_upload_size:
						raise forms.ValidationError(_('Please keep filesize under '+filesizeformat(self.max_upload_size)+'. Current filesize '+filesizeformat(file.size)) )
			else:
				content = ' ,'.join([str(elem) for elem in self.content_types]) 
				raise forms.ValidationError(_('Filetype not supported, make sure your content is ( '+content+' )'))
		except AttributeError:
			pass
		return data

class ContentTypeRestrictedFileFieldProtected(models.FileField):
	def __init__(self, *args, **kwargs):
		self.content_types = kwargs.pop("content_types", [])
		self.max_upload_size = kwargs.pop("max_upload_size", [])
		kwargs['storage'] = ProtectedFileSystemStorage()
		super(ContentTypeRestrictedFileFieldProtected, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(ContentTypeRestrictedFileFieldProtected, self).clean(*args, **kwargs)
		file = data.file
		try:
			content_type = file.content_type
			if content_type in self.content_types or self.content_types == []:
				if file.size > self.max_upload_size:
					raise forms.ValidationError(_('Please keep filesize under '+filesizeformat(self.max_upload_size)+'. Current filesize '+filesizeformat(file.size)) )
			else:
				content = ' ,'.join([str(elem) for elem in self.content_types]) 
				raise forms.ValidationError(_('Filetype not supported, make sure your content is ( '+content+' )'))
		except AttributeError:
			pass
		
		return data

def get_profile_path(instance,filename):
	# Generate filepath for new recipe image
	ext 		= filename.split('.')[-1]
	filename 	= f'{uuid.uuid4()}.{ext}'
	filename	= str(instance.id)+'/'+filename 

	return os.path.join('profile_pic/',filename)

# get file path to get course pic image upload path.
def get_course_pic_path(instance,filename):
	# Generate filepath for new recipe image
	ext 		= filename.split('.')[-1]
	filename 	= f'{uuid.uuid4()}.{ext}'
	filename	= str(instance.tutor.id) +'/'+filename
	return os.path.join('course_pic/',filename)
