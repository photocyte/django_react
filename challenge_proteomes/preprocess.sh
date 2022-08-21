#for f in ./*.txt
#do
# new_f=${f%.txt}
# mv $f $new_f
#done

#for f in ./*.faa
#do
#makeblastdb -dbtype prot -in $f

#done


##Have to be genetic code / trans_table aware
##This 
ls -1 ./NC*.faa | grep -v 'NC_023719' | xargs cat > merged_gc1.faa
ls -1 ./NC*.faa | grep 'NC_023719' | xargs cat > merged_gc11.faa ##This genome has translation table=11

for f in ./merged*.faa
do
/Users/tim/Source/git/diamond/bin/diamond makedb --in ${f} -d ${f}
done
