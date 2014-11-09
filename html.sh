#!/bin/sh
umask 022
time=$(date +%m%d%H%M)
for i in *.html */*.html 
do
    sed -i.bak -e "s|\(<.*src=.*\)\.js\(.*>\)|\1\.js\?time=$time\2|g" \
               -e "s|\(<.*href=.*\)\.css\(.*>\)|\1\.css\?time=$time\2|g" $i
done
