#!/bin/bash
#
# 用于设置新虚拟机的网络, $1 取 1~255, 但注意不要和已有虚拟机的 ip 重复了.
#

base_uuid="92e576d5-f199-4e5c-895c-a3f5f9ae821"
new_uuid="$((RANDOM % 100000000))-$((RANDOM % 10000))-$((RANDOM % 10000))-$((RANDOM % 10000))-$((RANDOM % 100000000000))"
new_ip="10.0.0."$1

sed_1_arg="/UUID=/s/.*/UUID=${new_uuid}/"
sed $sed_1_arg /etc/sysconfig/network-scripts/ifcfg-ens160 -in
sed_2_arg="/IPADDR=/s/.*/IPADDR=$new_ip"
sed $sed_2_arg /etc/sysconfig/netword-scripts/ifcfg-ens160 -in

echo "new uuid is: $new_uuid"
echo "new ip is: $new_ip"
