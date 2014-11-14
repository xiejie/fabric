#!/bin/sh
lynx -dump www.baidu.com | sed -n '/^References/,$p' | \
egrep -v "ftp://|javascript:|mailto:|news:|https://" | \
tail -n +5 | awk '{print $2}' | cut -d\? -f1 
