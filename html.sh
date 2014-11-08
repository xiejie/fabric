#!/bin/sh
umask 022
time=$(date +%m%d%H%M)
for i in *.html */*.html 
do
    sed -i.bak -e "s|\(<.*src=.*\)\.js\(\?.*\)\{0,1\}\(['\"]\)\(.*>\)|\1\.js\?time=$time\3\4|g" \
               -e "s|\(<.*href=.*\)\.css\(\?.*\)\{0,1\}\(['\"]\)\(.*>\)|\1\.css\?time=$time\3\4|g" $i
done
