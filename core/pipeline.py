from social_core.pipeline.partial import partial
from django.contrib.auth import get_user_model

@partial
def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        profile = user

        if profile.firstname ==  profile.lastname == '' :
            profile.username    = response.get('given_name').lower() + response.get('family_name').lower() + str(profile.id)
            profile.username    = profile.username.replace(' ', '_')
            
            profile.firstname   = response.get('given_name').lower()
            profile.lastname    = response.get('family_name').lower()
            profile.phone       = ''
        # # profile.profile_pic = response.get('picture')
            profile.save()

    # 'access_token': 'ya29.a0Ae4lvC2TTErk2Bd4NQvcpb3teRzSShsfzwYQSf1VBvLMsOX6hemQfEy228i97vc6SiadNtvuZxEbkJCPuNXtRCtyyxN7qqXrSUTP5eznaL8E4PI3a2SiWJsKZKbQU73JhYpBAYvhNdChmJ2DepDQ9T7-0qhdt2tQfAM',
    # 'email': 'dli@um.ac.id',
    # 'email_verified': True,
    # 'expires_in': 3599,
    # 'family_name': 'um',
    # 'given_name': 'dli',
    # 'hd': 'um.ac.id',
    # 'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjUzYzY2YWFiNTBjZmRkOTFhMTQzNTBhNjY0ODJkYjM4MDBjODNjNjMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNjQ4ODI1NDQ4NjEzLWIyMmUyb3Q3Yzc3ZWVobDlmMjJtOXJrZzA1dm1qYnE2LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNjQ4ODI1NDQ4NjEzLWIyMmUyb3Q3Yzc3ZWVobDlmMjJtOXJrZzA1dm1qYnE2LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA1OTcyMzc5MDQ2NTU5NTk0MjgyIiwiaGQiOiJ1bS5hYy5pZCIsImVtYWlsIjoiZGxpQHVtLmFjLmlkIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJqVWNqd0FWYTJFSWt1cDJDWFVMN0l3IiwiaWF0IjoxNTg1NjU0OTk4LCJleHAiOjE1ODU2NTg1OTh9.D2h7OO7R8xga8T4PLO9Qml03w5n3wcgjEbi16KZ7c6l6fbl5a4MpRaGdHHGIc36LKwR7onkALlmjUloee-NqVfYssSkCiGgJQOv2_YXyUM7jg7LjJlJG_lfm8qJpI-qrLwjnfC-eiyqEBs_SjWG2XusOJqsVnqflWeL-qw027fGJs_u2r40PS4lDOZF4Mt_T_rWx3enCzxbSD35dy03tfn-UR8M8RCghE7VEEtqb7N0812Akx8tOnhmBRACrORvahOw_P9X5f0bLCxrdLYBftW7zj0CbK_zh64C4f4hWvgL4zRRvevft9N1t1DzDUhfznDez0j3o1M2CSEeFfTcPfQ',
    # 'locale': 'en',
    # 'name': 'dli um',
    # 'picture': 'https://lh3.googleusercontent.com/a-/AOh14GiCGA__L7UCr3ua4LSKOLk7xg1Xvw6tEuxIX9AT',
    # 'scope': 'https://www.googleapis.com/auth/userinfo.email '
    # 'https://www.googleapis.com/auth/userinfo.profile openid',
    # 'sub': '105972379046559594282',
    # 'token_type': 'Bearer'

    # firstname	= models.CharField(max_length=256,default='')
	# lastname	= models.CharField(max_length=256,default='')
	# email		= models.EmailField(max_length=256,unique=True)
	# password	= models.CharField(max_length=256)

	# biography	= models.TextField(default='',blank=True)
	# languange	= models.ForeignKey(Languange,on_delete=models.CASCADE,null=True)

	# website		= models.CharField(max_length=256,default='',blank=True)
	# twitter		= models.CharField(max_length=256,default='',blank=True)
	# facebook	= models.CharField(max_length=256,default='',blank=True)
	# linkedin	= models.CharField(max_length=256,default='',blank=True)
	# youtube		= models.CharField(max_length=256,default='',blank=True)

	# is_active	= models.BooleanField(default=True) 
	# is_user		= models.BooleanField(default=True) 
	# is_staff	= models.BooleanField(default=False) 
	# is_tutor	= models.BooleanField(default=False)
	# profile_pic = models.ImageField(upload_to=get_file_path,null=True,blank=True)