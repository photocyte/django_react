from django.shortcuts import render

# Create your views here.

from .models import Lead
from .models import DNA_Protein_Alignment_Query
from .serializers import LeadSerializer
from .serializers import DNAQuerySerializer
from rest_framework import generics
import threading
import Bio

## https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all() 
    serializer_class = LeadSerializer

class QueryListCreate(generics.ListCreateAPIView):
    queryset = DNA_Protein_Alignment_Query.objects.all() 
    serializer_class = DNAQuerySerializer

    def execute_dna_to_protein_alignment(self,dna_seq):
        ## See https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create
        print("THREADS!",dir(self))
        #print(self.get_serializer().get_instance())
        #print(dir(self.get_serializer().update()))

        model_rows = self.get_queryset() ##TODO: Rather than looking up based on the last index, should lookup based on datetime
        max_index = len(model_rows)
        print(model_rows.filter(id=max_index).values())
        assert dna_seq == model_rows.filter(id=max_index).values()['query_seq']
        ## https://docs.djangoproject.com/en/4.1/ref/models/querysets/#update
        model_rows.filter(id=max_index).update(alignment_status="RUNNING")

        #most_recent_model = list(model_rows)[-1]
        #print(dir(most_recent_model))
        #most_recent_model.update(status="RUNNING")


        return None

    ##Override the create() function to kick off a DNA alignment whenever a new sequence arrives
    def create(self, request):
        return_val = super().create(request)
        # Note the use of `get_queryset()` instead of `self.queryset`
        #queryset = self.get_queryset()
        dna_seq = request.data['query_seq']
        print(dna_seq)
        thread = threading.Thread(target=self.execute_dna_to_protein_alignment, args=(dna_seq,))
        thread.start()
        print("OVERRIDDEN!",request.data)
        

        return return_val
