from rest_framework import serializers
from core.models import Schedule,Category,Course,Order
from django.contrib.auth import get_user_model

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields  = ('id','username','email',)

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Category
        fields  = ('id','name','image')

class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Course
        # fields  = ('id','title','price',)
        fields  = ('id','title','price','description','category','course_pic','course_type','start_at','close_at',)

class UserOrderModelSerializer(serializers.ModelSerializer):
    course          = CourseModelSerializer()
    
    class Meta:
        model   = Order
        fields  = ('id','invoice_no','course','price','transaction_url','status',)

class MentorScheduleModelSerializer(serializers.ModelSerializer):
    mentor  = UserModelSerializer(read_only=True,required=False)

    class Meta:
        model   = Schedule
        fields  = ('id','mentor','day','time',)

    # def create(self, validated_data):
    #     return Schedule.objects.create(**validated_data)