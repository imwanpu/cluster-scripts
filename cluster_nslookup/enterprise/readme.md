## cluster_nslookup

a tool for querying DNS records on hosts in a cluster.

一个用于在集群中各个主机进行批量DNS查询的脚本

## Role of Important File 重要文件的作用

- `playbook.yaml`: describing the execution process 描述执行步骤, 使用 ansible-playbook 运行这个文件
- `serial_nslookup.sh`: generating DNS resolution data `/tmp/ansible/serial_nslookup_host_result.txt` on each host in cluster 在集群中的每台主机上, 生成 DNS 查询结果到 `/tmp/ansible/serial_nslookup_host_result.txt`
- `parser.py`: parsing the collected data `/tmp/serial_nslookup_data/` to the file `./cluster_nslookup/result.txt` 将收集在 `/tmp/serial_nslookup_data/` 目录下的数据文件解析, 将解析后的数据存储在 `./cluster_nslookup/result.txt` 中
- `domains.txt`: domains that require DNS resolution on each host in the cluster 需要在集群中每台主机上进行 DNS 查询的域名
- `inventory.ini`: list of host to be operated in the cluster 需要操作的主机列表
- `result.txt`: final result 最终数据

## How to Use

Modify the `domains.txt` and `inventory.ini` files as needed.

根据需要修改domains.txt和inventory.ini这两个文件


```shell
rm -rf ./result.txt && ansible-playbook -i ./inventory.ini ./playbook.yaml
ansible-playbook -i inventory.ini playbook.yaml --extra-vars "elapsed=60 interval=3"   
cat ./result.txt
```
## TODO

- [x] 修复不存在DNS记录域名不显示的问题
- [x] 修复 yaml 文件执行时的用 ansible file 模块替代 shell -a 'rm -rf' 警告


## FAQ(Frequently Asked Questions)

### 未安装 nslookup

**Handling Method 处理方法**

```shell
yum install bind-utils
```