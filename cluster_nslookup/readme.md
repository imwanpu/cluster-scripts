## cluster_nslookup

a tool for querying DNS records on hosts in a cluster.

一个用于在集群中各个主机进行批量DNS查询的脚本

## tldr

```shell
rm -rf ./*_result.txt ./*_sorted_result.txt
ansible-playbook -i ./inventory.ini ./playbook.yaml --extra-vars "elapsed=3600 interval=16 dns_timeout=1 dns_retry=1" &
ansible-playbook -i ./inventory.ini ./show_me_now.yaml
```

## Role of Important File 重要文件的作用

- `playbook.yaml`: describing the execution process 描述执行步骤, 使用 ansible-playbook 运行这个文件
- `serial_nslookup.sh`: generating DNS resolution data `/tmp/ansible/serial_nslookup_host_result.txt` on each host in cluster 在集群中的每台主机上, 生成 DNS 查询结果到 `/tmp/ansible/serial_nslookup_host_result.txt`
- `parser.py`: parsing the collected data `/tmp/serial_nslookup_data/` to the file `./cluster_nslookup/result.txt` 将收集在 `/tmp/serial_nslookup_data/` 目录下的数据文件解析, 将解析后的数据存储在 `./cluster_nslookup/result.txt` 中
- `domains.txt`: domains that require DNS resolution on each host in the cluster 需要在集群中每台主机上进行 DNS 查询的域名
- `inventory.ini`: list of host to be operated in the cluster 需要操作的主机列表
- `result.txt`: unsorted aggregate data 未排序的汇总数据
- `sorted_date.txt`: sorted aggregate data 经过排序的最终数据

## How to Use 使用说明

1. Modify the `domains.txt` and `inventory.ini` files as needed. 根据需要修改domains.txt和inventory.ini这两个文件

2. Run the collection script `playbook.yaml`. 运行收集脚本 `playbook.yaml`

```shell
rm -rf ./*_result.txt ./*_sorted_result.txt && 
ansible-playbook -i ./inventory.ini ./playbook.yaml --extra-vars "elapsed=3600 interval=16 dns_timeout=1 dns_retry=1" &
```

During the execution of the collection script, you can also temporatily view the data, and the command are as follows. The resultss are stored in files staring with the time as `*_result.txt` and `*_sorted_result.txt`. 在运行收集脚本 `playbook.yaml` 的过程中, 也可以临时查看数据, 命令如下, 结果存储在以时间为开头的 `*_result.txt` 和 `*_sorted_result.txt` 文件中

```shell
ansible-playbook -i ./inventory.ini ./show_me_now.yaml
```

Explanation of `./playbook.yaml` parameters. `./playbook.yaml` 参数说明

- `elapsed`: total time for scheduled DNS resolution script running on each host in the cluster.集群中每台主机上运行定时DNS解析脚本的总时间
- `interval`: interval time for collecting DNS resolution data on each host in the cluser. 集群中每台主机上收集DNS解析数据的间隔时间
- `dns_timeout`: the `timeout` parameter of `nslookup`. `nslookup` 的 `timeout` 参数 
- `dns_retry`: the `retry` parameter of `nslookup`. `nslookup` 的 `retry` 参数


## TODO

- [x] 修复不存在DNS记录域名不显示的问题
- [x] 修复 yaml 文件执行时的用 ansible file 模块替代 shell -a 'rm -rf' 警告
- [x] 添加时间控制功能
- [x] 添加试试查看功能
- [ ] ~~是否清理本机收集到的数据~~

## NOTES

**Pay attention to your disk space! 注意磁盘空间占用**

When using three hosts to perform DNS queries on three domains with a three-secend interval for one hour, the `result.txt` file size is 1MB, the `sorted_result.txt` file size is 1MB, and each host in the cluster occupies 1MB of disk space in the `/tmp/ansible/` directory. Of course, the above is just a casual and imprecise samall experiment.

当使用三台主机, 对三条域名, 以三秒为间隔, 进行一小时的 DNS 查询, `result.txt` 文件大小为 1MB, `sorted_result.txt` 文件大小为 1MB, 集群中各主机的 `/tmp/ansible/` 目录占用 1MB 磁盘空间. 当然, 上面只是一个不严谨的小实验.


## FAQ(Frequently Asked Questions)

### 未安装 nslookup

**Handling Method 处理方法**

```shell
yum install bind-utils
```