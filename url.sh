#!/bin/sh
if [ $# -ne 1 ]
then
    echo "Usage: $0 url"
    exit 1
fi

lynx -dump $1 | sed -n '/^References/,$p' | \
egrep -v "ftp://|javascript:|mailto:|news:|https://|^$|links:" | \
tail -n +5 | awk '{print $2}' | cut -d\? -f1 
