#!/bin/bash
#
# 用于设置新虚拟机的网络, $1 取 1~255, 但注意不要和已有虚拟机的 ip 重复了.
#

base_uuid="92e576d5-f199-4e5c-895c-a3f5f9ae821"
new_uuid="$((RANDOM % 100000000))-$((RANDOM % 10000))-$((RANDOM % 10000))-$((RANDOM % 10000))-$((RANDOM % 100000000000))"
new_ip="10.0.0."$1
new_hostname="h"$1

sed_1_arg="/UUID=/s/.*/UUID=${new_uuid}/p"
sed $sed_1_arg /etc/sysconfig/network-scripts/ifcfg-ens33 -in
sed_2_arg="/IPADDR=/s/.*/IPADDR=$new_ip/p"
sed $sed_2_arg /etc/sysconfig/network-scripts/ifcfg-ens33 -in
hostname $new_hostname

echo "new uuid is: $new_uuid"
echo "new ip is: $new_ip"
echo "new hostname is: "
systemctl restart network
systemctl disable firewalld
systemctl stop firewalld
ip addr
hostname
