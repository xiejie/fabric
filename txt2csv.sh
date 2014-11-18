#!/bin/sh
OUT=`echo $1|cut -d. -f1`
COUNT=`awk -F"\t" '{if (NR==1) print NF}' $1`
cat $1 | awk 'BEGIN {FS="\t";OFS="\",\""} {print "\""$1,$2,$3,$4,$5"\"" }' > $OUT.csv 
