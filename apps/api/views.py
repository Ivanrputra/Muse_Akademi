from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.http import Http404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

# import datetime

from core.models import Category,Course,Order,Schedule

from .permission import ReadOnly,IsAuthenticated,IsAuthenticatedOrReadOnly, \
    IsMentorOwner,IsAdminOwner,IsMentorOrStaff
from . import serializers
from .pagination import CustomPagination

# Create your views here.

class CategoryView(viewsets.ReadOnlyModelViewSet):
    permission_classes  = [ReadOnly]
    renderer_classes    = [JSONRenderer]

    queryset            = Category.objects.all()
    serializer_class    = serializers.CategoryModelSerializer

class CourseView(viewsets.ModelViewSet):
    pagination_class    = CustomPagination
    permission_classes  = [IsAuthenticated]
    # renderer_classes    = [JSONRenderer]

    queryset            = Course.objects.all()
    serializer_class    = serializers.CourseModelSerializer

    # filter_backends = (SearchFilter,)
    # search_fields = ('category__id',)

    # filter_backends = (DjangoFilterBackend,)
    # search_fields = ('title',)

    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('category'):
            params = self.request.query_params.get('category').split(",")
            queryset = queryset.filter(category__in=params)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)
        

class UserCourseView(viewsets.ReadOnlyModelViewSet):
    pagination_class    = CustomPagination
    permission_classes  = [IsAuthenticated]
    renderer_classes    = [JSONRenderer]

    serializer_class    = serializers.CourseModelSerializer

    def get_queryset(self):
        queryset = Course.objects.filter(library__user=self.request.user)
        if self.request.query_params.get('status'):
            if self.request.query_params.get('status') == "active":
                queryset = queryset.filter(start_at__gte=timezone.now(),close_at__lte=timezone.now())
            elif self.request.query_params.get('status') == "done":
                queryset = queryset.filter(close_at__gte=timezone.now())
            elif self.request.query_params.get('status') == "soon":
                queryset = queryset.filter(start_at__lte=timezone.now())
        return queryset

class UserOrderView(viewsets.ReadOnlyModelViewSet):
    pagination_class    = CustomPagination
    permission_classes  = [IsAuthenticated]
    renderer_classes    = [JSONRenderer]

    serializer_class    = serializers.UserOrderModelSerializer

    # filter_backends = (SearchFilter,)
    # search_fields = ('status',)

    def get_queryset(self):
        queryset    =  Order.objects.filter(user=self.request.user)
        if self.request.query_params.get('status'):
            queryset = queryset.filter(status__contains=self.request.query_params.get('status'))
        return queryset

class MentorScheduleView(viewsets.ModelViewSet):
    # pagination_class    = CustomPagination
    permission_classes  = [IsMentorOrStaff]
    # renderer_classes    = [JSONRenderer]

    serializer_class    = serializers.MentorScheduleModelSerializer

    def get_queryset(self):
        if self.request.query_params.get('mentor') and self.request.user.is_staff:
            queryset    =  Schedule.objects.filter(mentor__id=int(self.request.query_params.get('mentor')))
        else:
            queryset    =  Schedule.objects.filter(mentor=self.request.user)

        if self.request.query_params.get('status'):
            queryset = queryset.filter(status__contains=self.request.query_params.get('status'))
        return queryset
    
    def perform_create(self, serializer):
        print(serializer.validated_data)
        serializer.save(mentor=self.request.user)

    # def create(self, serializer):
    #     serializer.save(user=self.request.user)

# {
#     "day": "MO",
#     "time": "00:11:38"
# }


# class CategoryView(APIView):
#     permission_classes = [ReadOnly]
#     @csrf_exempt
#     def get(self, request, format=None):
#         category = Category.objects.all()
#         serializer = serializers.CategoryModelSerializer(category, many=True)
#         return Response(serializer.data)

#     create()`, `retrieve()`, `update()`,`partial_update()`, `destroy()` and `list()` actions.
# class Category(ModelViewSet):
#     permission_classes = [ReadOnly]
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategoryModelSerializer
#     allowed_methods = ('GET', 'HEAD', 'OPTIONS')
#     pagination_class = None  # Get all user