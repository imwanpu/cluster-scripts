#!/bin/bash
for i in {1..600}; do
    IP=$(hostname -I | awk '{print $1}')
    echo Test baidu.com From $IP
    echo $i && date && time nslookup baidu.com 114.114.114.114 | grep time
    echo Test zhihu.com From $IP
    echo $i && date && time nslookup zhihu.com 114.114.114.114 | grep time
    sleep 3
done
