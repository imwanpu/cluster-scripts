#!/bin/bash
#
## 并行 nslookup domains.txt 中的域名

domains_file="/tmp/ansible/domains.txt"
dns="114.114.114.114"
tmp_file="/tmp/ansible/serial_nslookup_host_result.txt"

domains=$(cat ${domains_file})
if [ -f "${tmp_file}" ]; then
    rm ${tmp_file}
    touch ${tmp_file}
fi
host_ip=$(hostname -I | awk '{print $1}')

printf "Host IP\t%s\n" "${host_ip}" >"${tmp_file}"
for domain in ${domains}; do
    # nslookup_result=$(time nslookup "${domain}" ${dns} 2>&1)
    # echo "${nslookup_result}"
    (time nslookup "${domain}" ${dns}) >>"${tmp_file}" 2>&1
    date >>"${tmp_file}"
    # awk '
    #     {count[$1] += $2};
    #     END{
    #         for (key in count) {printf("%s\t\t", key)}
    #         printf("\n")
    #         for (key in count) {printf("%s\t\t", count[key])}
    #         printf("\n")
    #     }
    # ' ${tmp_file}
done

exit 0
