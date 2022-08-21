from django.db import models
from django.core.validators import RegexValidator
import re

# Create your models here.

#See https://docs.djangoproject.com/en/4.1/topics/db/models/#module-django.db.models


class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300) 
    created_at = models.DateTimeField(auto_now_add=True)

def validate_dna(value):
    #print(value.encode('utf-8'))
    new_value = value.replace('\n','').replace('\r','').strip() ## Look, I shouldn't have to call this because the Django docs say to_python() is run before this, yet I have to.
    dna_vali = RegexValidator(r'^[actgACTGnN]+$','Must be a DNA sequence of only ACTG.')
    dna_vali(new_value)

class DNAQuerySeqField(models.CharField):

    ##Override the to_python function https://docs.djangoproject.com/en/4.1/ref/forms/validation/
    def to_python(self, value):
        new_value = value.replace('\n','').replace('\r','').strip()
        return new_value

class DNA_Protein_Alignment_Query(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    query_seq = DNAQuerySeqField(max_length=30000,validators=[validate_dna]) ## ,validators=[dna_vali]
    alignment_status = models.CharField(max_length=3000,default='RECIEVED')
    #alignment_status = models.TextChoices('status','RECIEVED STARTED FINISHED ERROR') 
    results = models.CharField(max_length=300,blank=True,default="(no results yet)")  
    