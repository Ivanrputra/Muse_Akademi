from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer
from rest_framework import generics

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
from rest_framework import viewsets


from core.models import Category

from .permission import ReadOnly,IsAuthenticated,IsAuthenticatedOrReadOnly, \
    IsMentorOwner,IsAdminOwner
from . import serializers



# Create your views here.

# class CategoryView(APIView):
#     permission_classes = [ReadOnly]
#     @csrf_exempt
#     def get(self, request, format=None):
#         category = Category.objects.all()
#         serializer = serializers.CategoryModelSerializer(category, many=True)
#         return Response(serializer.data)

class CategoryView(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    permission_classes  = [ReadOnly]
    renderer_classes    = [JSONRenderer]

    queryset            = Category.objects.all()
    serializer_class    = serializers.CategoryModelSerializer

#     create()`, `retrieve()`, `update()`,`partial_update()`, `destroy()` and `list()` actions.
# class Category(ModelViewSet):
#     permission_classes = [ReadOnly]
#     queryset = Category.objects.all()
#     serializer_class = serializers.CategoryModelSerializer
#     allowed_methods = ('GET', 'HEAD', 'OPTIONS')
#     pagination_class = None  # Get all user