from django.db import models
import re

# Create your models here.

#See https://docs.djangoproject.com/en/4.1/topics/db/models/#module-django.db.models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300) 
    created_at = models.DateTimeField(auto_now_add=True)

def validate_dna(value):
    re.search()
    ##TODO implement as RegexValidator as per https://docs.djangoproject.com/en/4.1/ref/validators/

class DNA_Alignment_Query(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    query_seq = models.CharField(max_length=30000,validators=[validate_dna]) ## Need to use a custom field.clean() method, to strip it of newlines etc. 
    #alignment_status = models.TextChoices('RECIEVED','STARTED', 'FINISHED', 'ERROR',default='RECIEVED') 
    results = models.CharField(max_length=300,blank=True,default="(no results yet)")  
    