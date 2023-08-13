#!/bin/bash

result_file="/tmp/cluster_nslookup_v0.2/result.txt"
dnss_file="/tmp/cluster_nslookup_v0.2/dnss.txt"
domains_file="/tmp/cluster_nslookup_v0.2/domains.txt"
elapsed=$1
interval=$2
timeout=$3
retry=$3

dnss=$(cat "${dnss_file}")
domains=$(cat "${domains_file}")

for i in $(seq 0 "${interval}" "${elapsed}"); do
    for dns in ${dnss}; do
        for domain in ${domains}; do
            date=$(date +%Y-%m-%d_%H:%M:%S)
            resutl_time_nslooup=$({ time nslookup -timeout="${timeout}" -retry="${retry}" "${domain}" "${dns}"; } 2>&1)
            line_result=$(echo "${resutl_time_nslooup}" | awk 'BEGIN {ORS="@@@"} NF')
            echo "${date}@@@${line_result}@@@arg_domain: ${domain}@@@arg_dns: ${dns}" >>${result_file}
        done
    done
    sleep "${interval}"
done
