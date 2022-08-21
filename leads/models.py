from django.db import models
from django.core.validators import RegexValidator

## For Token authentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

## For cookie authentication
# https://yoongkang.com/blog/cookie-based-authentication-spa-django/
# https://www.guguweb.com/2022/01/23/django-rest-framework-authentication-the-easy-way/

# Create your models here.

#See https://docs.djangoproject.com/en/4.1/topics/db/models/#module-django.db.models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=300) 
    created_at = models.DateTimeField(auto_now_add=True)

def validate_dna(value):
    #print(value.encode('utf-8'))
    new_value = value.replace('\n','').replace('\r','').strip() ## Look, I shouldn't have to call this because the Django docs say to_python() is run before this, yet that doesn't happen in my hands.
    dna_vali = RegexValidator(r'^[actgACTGnN]+$','Failure. Must be a DNA sequence of only ACTG.')
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

### Below is Failed attempt at token authentication. Vestigial. 
## See https://www.django-rest-framework.org/api-guide/authentication/#generating-tokens
#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    if created:
#        Token.objects.create(user=instance) 