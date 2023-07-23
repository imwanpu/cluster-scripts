#!/bin/bash
#
# 通过二进制安装包安装 mysql
# 仅在 CentOS 7.9 中使用过
#

## 你可能需要修改的变量
using_network="no" # 如果需要从网络中下载 `mysql-5.7.43-linux-glibc2.12-x86_64.tar.gz` 文件, 将此参数改为 yes
# 如果在脚本所在目录下有 `mysql-5.7.43-linux-glibc2.12-x86_64.tar.gz`, 则无需下载
mysql_startup="yes"

## 你最好不要修改这些变量
script_abs_path=$(dirname "$(readlink -f "$0")")

mysql_version="5.7.43"
mysql_package_name="mysql-${mysql_version}-linux-glibc2.12-x86_64.tar.gz"
mysql_package_uri="${script_abs_path}/${mysql_package_name}"
mysql_package_path="${script_abs_path}"
mysql_root_passwd="p0-p0-P0-"
mysql_base="/usr/local/mysql"

# 检查是否有 mysql glibc 文件, 如果没有, 就报错 写warning信息, 如果有使用网络的参数, 就从网络下载

# 使用网络前 TODO
# if [ "${using_network}" = "yes" ]; then
#     yum install -y wget
#     download_url="https://cdn.mysql.com//Downloads/MySQL-5.7/"${mysql_package_name}
#     wget ${download_url}
#     if $? ; then
#         echo $LINENO; exit 1
#     fi
# fi

## 判断安装包是否存在
if [ -f ${mysql_package_uri} ]; then
    echo "[OK] - ${mysql_package_uri}} was found"
else
    echo "${mysql_package_uri} ws not found "
    echo "error in line $LINENO"
    exit 1
fi

## 删除 /etc/my.cnf
if [ -f "/etc/my.cnf" ]; then
    rm -rf /etc/my.cnf
    echo "[OK] - /etc/my.cnf has been removed"
else
    echo "[OK] - /etc/my.cnf has been removed"
fi

## 官网的安装步骤
# if getent group mysql; then
#     groupdel mysql
#     echo "[OK] - the old mysql user group has been deleted"
# fi
groupadd mysql
echo "[OK] - a new mysql user group has been created"
useradd -r -g mysql -s /bin/false mysql
cp "${mysql_package_uri}" "/usr/local/${mysql_package_name}"
mkdir /usr/local/mysql-${mysql_version}
tar -zxvf /usr/local/${mysql_package_name} -C /usr/local
ln -s /usr/local/${mysql_package_name%.tar.gz} /usr/local/mysql
mkdir /usr/local/mysql/mysql-files
chown mysql:mysql /usr/local/mysql/mysql-files
chmod 750 /usr/local/mysql/mysql-files
log=$(${mysql_base}/bin/mysqld --initialize --user=mysql 2>&1)
${mysql_base}/bin/mysql_ssl_rsa_setup
${mysql_base}/bin/mysqld_safe --user=mysql >/usr/local/mysql/mysqlroot.log &
sleep 5
cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql.server
touch /usr/local/mysql/my.cnf

## 拿到默认密码
temporaty_pssword=$(echo $log | awk -F "root@localhost: " '/root@localhost/{print $2}')
echo "[OK] - the initialization password is: $temporaty_pssword"

# 根据默认密码修改密码
/usr/local/mysql/bin/mysqladmin -u root --password="${temporaty_pssword}" password "${mysql_root_passwd}"

echo "export PATH=\$PATH:/usr/local/mysql/bin" >>/etc/bashrc
source /etc/bashrc
