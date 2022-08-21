from django.shortcuts import render

# Create your views here.

from .models import Lead
from .serializers import LeadSerializer
from rest_framework import generics

## https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all() 
    serializer_class = LeadSerializer

