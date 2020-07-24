from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

from core.models import Category
from .permission import ReadOnly,IsAuthenticated
from . import serializers


# Create your views here.

class Category(APIView):
    permission_classes = [ReadOnly]
    @csrf_exempt
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = serializers.CategoryModelSerializer(category, many=True)
        return Response(serializer.data)

# class Category(ModelViewSet):
#     permission_classes = [ReadOnly]
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategoryModelSerializer
#     allowed_methods = ('GET', 'HEAD', 'OPTIONS')
#     pagination_class = None  # Get all user