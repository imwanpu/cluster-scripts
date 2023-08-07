#!/bin/bash

file_name="/tmp/host_be_ping.txt" # WARNING 文件最后留个空行
ping_count=3
ping_wait=$(hostname -i)
is_all_ip=$1
host_ip=$(hostname -i)

if [[ "${is_all_ip}" == "-a" ]]; then
    host_ip=$(ip -o -4 addr show scope global | awk '{split($4, a, "/"); print a[1]}')
fi




results=()
host_be_ping=$(cat $file_name)


for host in ${host_be_ping}; do
    
    if ping_result=$(ping -c ${ping_count} -W ${ping_wait} ${host}); then
        # echo -e $ping_result
        result=$(sed -n 's/.* \([0-9.]\+\)% packet loss.*/\1/p' <<< ${ping_result})
        echo "${host_ip} -> ${host} is OK"                  
    else
        # echo -e $ping_result
        result=$(sed -n 's/.* \([0-9.]\+\)% packet loss.*/\1/p' <<< ${ping_result})
        echo "${host_ip} -> ${host} is not OK"          
    fi & # 后台执行
done

wait


for result in "${results[@]}"
do
  echo "$result"
done
