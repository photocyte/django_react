from rest_framework import serializers
from .models import Lead
from .models import DNA_Protein_Alignment_Query

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name', 'email', 'message')

class DNAQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = DNA_Protein_Alignment_Query
        fields = ('id', 'query_seq', 'alignment_status', 'results')