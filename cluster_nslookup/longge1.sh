#!/bin/bash

for i in {1..3600}; do
    echo $i && date && time nslookup baidu.com 114.114.114.114
    echo $i && date && time nslookup zhihu.com 8.8.8.8
    sleep 3
done
