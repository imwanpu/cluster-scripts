#!/bin/bash
#
## 并行 nslookup domains.txt 中的域名

domains_file="/tmp/ansible_serial_nslookup/domains.txt"
dns="114.114.114.114"
tmp_file="/tmp/ansible_serial_nslookup/serial_nslookup_host_result.txt"
total_time=$1
interval_time=$2
timeout=$3
retry=$4

domains=$(cat ${domains_file})
if [ -f "${tmp_file}" ]; then
    rm ${tmp_file}
    touch ${tmp_file}
fi
host_ip=$(hostname -I | awk '{print $1}')

printf "Host IP\t%s\n" "${host_ip}" >"${tmp_file}"

count=0
while [ $count -lt "${total_time}" ]; do
    for domain in ${domains}; do
        (time nslookup -timeout="${timeout}" -retry="${retry}" "${domain}" ${dns}) >>"${tmp_file}" 2>&1
        date +%Y-%m-%d_%H:%M:%S >>"${tmp_file}"
    done
    count=$((count + interval_time))
    sleep "${interval_time}"
done

exit 0
