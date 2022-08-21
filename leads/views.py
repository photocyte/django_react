from django.shortcuts import render

# Create your views here.

from .models import Lead
from .models import DNA_Protein_Alignment_Query
from .serializers import LeadSerializer
from .serializers import DNAQuerySerializer
from rest_framework import generics

## https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all() 
    serializer_class = LeadSerializer

class QueryListCreate(generics.ListCreateAPIView):
    queryset = DNA_Protein_Alignment_Query.objects.all() 
    serializer_class = DNAQuerySerializer