from django.shortcuts import render

# Create your views here.

from .models import DNA_Protein_Alignment_Query
from . import serializers
from rest_framework import generics
import threading
import subprocess

import Bio
import Bio.SeqIO
import Bio.SeqUtils
import Bio.pairwise2
##import Bio.Align.substitution_matrices 

from rest_framework import permissions, views, status
from rest_framework.response import Response

from django.contrib.auth import login
import glob
import re
import shlex
from io import StringIO 

## Just has to run these early somewhere & then be use them as global variables. Seems a decent place!
#fasta_to_transl_table_dict = {'NC_000852.faa':1,'NC_007346.faa':1,'NC_008724.faa':1,'NC_009899.faa':1,'NC_014637.faa':1,'NC_016072.faa':1,'NC_020104.faa':1,'NC_023423.faa':1,'NC_023719.faa':1,'NC_027867.faa':1}
#fasta_to_transl_table_dict = {'./challenge_proteomes/' + str(key): val for key, val in fasta_to_transl_table_dict.items()} ## Add a prefix for where they are path-wise
#preloaded_fastas = { k:Bio.SeqIO.parse(k,"fasta") for k in fasta_to_transl_table_dict.keys() }
preloaded_fastas = { re.findall('.+gc([0-9]+).+',f)[0]:f for f in glob.glob('./challenge_proteomes/merged*.faa') } ## <-- the preprocess.sh script merges the files based on genetic code

#BLOSUM62_matrix = Bio.Align.substitution_matrices.load('BLOSUM62')

##I tried to override, or decorate the Bio.SeqUtils.six_frame_translations , since I want the actual sequence not its default pretty print thing
## https://levelup.gitconnected.com/method-and-function-overriding-in-python-96a000274248
## But I couldn't figure it out. Has something to do with Bio.SeqUtils being both a class and module simultaneously?
## Anyway, below is a reimplementation where it returns what I want.
def six_frame_translate(seq,genetic_code):
    from Bio.Seq import reverse_complement, translate


    anti = reverse_complement(seq)
    comp = anti[::-1]
    length = len(seq)
    frames = {}
    for i in range(0, 3):
        fragment_length = 3 * ((length - i) // 3)
        frames[i + 1] = translate(seq[i : i + fragment_length], genetic_code)
        frames[-(i + 1)] = translate(anti[i : i + fragment_length], genetic_code)[::-1]
    return frames

## https://www.django-rest-framework.org/api-guide/generic-views/#listcreateapiview
class QueryListCreate(generics.ListCreateAPIView):
    queryset = DNA_Protein_Alignment_Query.objects.all() 
    serializer_class = serializers.DNAQuerySerializer

    def execute_dna_to_protein_alignment(self,dna_seq):
        ## See https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-perform-create

        model_rows = self.get_queryset() 
        max_index = len(model_rows) ##TODO: Rather than looking up based on the last index, should lookup based on datetime

        ## https://docs.djangoproject.com/en/4.1/ref/models/querysets/#update
        model_rows.filter(id=max_index).update(alignment_status="RUNNING")

        merged_outs = b''
        for k,v in preloaded_fastas.items():
            #diamond_cmd='apptainer exec ./diamond_2.0.15--hb97b32f_1.sif diamond blastx --ultra-sensitive --evalue 9999999 --query-gencode {gc} --db {db}'.format(gc=k,db=v) ##diamond will read the query in FASTA format from stdin.
            blastx_cmd='apptainer exec ./blast_2.13.0--hf3cf87c_0.sif blastx -query_gencode {gc} -word_size 2 -outfmt 6 -evalue 999999999999 -num_alignments 1 -query /dev/stdin -subject {db}'.format(gc=k,db=v)
            cmd_list = shlex.split(blastx_cmd)
            print(cmd_list)
            search_process = subprocess.Popen(cmd_list,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            query = '>{hash}\n{seq}'.format(hash='QuerySeqID',seq=dna_seq).encode('utf-8') ##hash(dna_seq)
            search_process.communicate(input=query)
            outs, errs = search_process.communicate()
            #print(outs,errs)
            #print(search_process.returncode)
            #print(outs,type(outs))
            if outs != None:
                merged_outs += outs
        merged_outs = merged_outs.strip()
        print(merged_outs)
        merged_outs = merged_outs.decode('utf-8')
        if len(merged_outs) == 0:
            merged_outs = '(no hits)'
        model_rows.filter(id=max_index).update(alignment_status="COMPLETE")
        model_rows.filter(id=max_index).update(results=merged_outs)
        ### Below is a direct search using biopython. It's too slow. I'll just call blastx or diamond instead.
        ##
        ##v in this case is the different genetic codes / trans_table:
        #six_frame_precalc = {}
        #for v in set(fasta_to_transl_table_dict.values()):
        #    six_frame_precalc[v] = six_frame_translate(dna_seq,v)

        ## k = the fasta paths
        #for k in preloaded_fastas:
        #    for r in preloaded_fastas[k]:
        #        for v in six_frame_precalc:
        #            for f in six_frame_precalc[v]:
        #                f, q = (f,six_frame_precalc[v][f]) ## v is the genetic code, f is the frame
        #                print("QUERY GENETIC CODE:",v)
        #                print("QUERY TRANS FRAME:",f)
        #                print("QUERY SEQ:",q)
        #                print("TARGET SEQ:",r.seq)
        #                print(Bio.pairwise2.align.localdx(q, r.seq, BLOSUM62_matrix))

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

        return return_val

## Tried to get session based authentication / cookies to work.
#class LoginView(views.APIView):
#    # This view should be accessible also for unauthenticated users.
#    permission_classes = (permissions.AllowAny,)
#
#    def post(self, request, format=None):
#        serializer = serializers.LoginSerializer(data=self.request.data,
#            context={ 'request': self.request })
#        serializer.is_valid(raise_exception=True)
#        user = serializer.validated_data['user']
#        login(request, user)
#        return Response(None, status=status.HTTP_202_ACCEPTED)
