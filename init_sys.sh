#!/bin/bash
#

if [ $# -lt 2 ]; then
    echo "Usage: sh $0 user_name user_password"
    exit 1
fi


#初始化变量
ROOT_PASS="kjhl"
USER_NAME=$1
USER_PASS=$2
HOST_LIST="10.0.0.12 10.0.0.13"


# 第一步: 管理主机本地创建用户, 设置密码
useradd $1
echo $USER_PASS | passwd --stdin $USER_NAME


# 第二步: 管理主机创建的用户生成密钥对
su - $USER_NAME -c "echo "" | ssh-keygen -t rsa"
PUB_KEY="$(cat ~/.ssh/id_rsa.pub)"

# 第三步: 利用 SSH 非免密在所有主机创建用户
# 第四步: 利用 SSH 非面命将管理主机公钥写入所有主机的 authorized_keys 文件

for host in $HOST_LIST; do
    sshpass -p$ROOT_PASS ssh -o StrictHostKeyChecking=no root@$host "useradd $USER_NAME"
    sshpass -p$ROOT_PASS ssh -o StrictHostKeyChecking=no root@$host "echo "$USER_PASS" | passwd --stdin $USER_NAME"
    sshpass -p$ROOT_PASS ssh -o StrictHostKeyChecking=no root@$host "mkdir /home/$USER_NAME/.ssh -pv"
    sshpass -p$ROOT_PASS ssh -o StrictHostKeyChecking=no root@$host "echo $PUB_KEY > /home/$USER_NAME/.ssh/authorized_keys"
    sshpass -p$ROOT_PASS ssh -o StrictHostKeyChecking=no root@$host "chmod 600 /home/$USER_NAME/.ssh/authorized_keys"
    sshpass -p$ROOT_PASS ssh -o StrictHostKeyChecking=no root@$host "chown -R $USER_NAME:$USER_NAME /home/$USER_NAME/.ssh"

done    