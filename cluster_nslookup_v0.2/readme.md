

## TLDR

```shell

```

## 使用步骤

在集群中的各个主机上运行脚本, 在指定时间后, 脚本将运行结束, 结果保存在 `playbook.yaml` 文件目录下, 形如 `2023-08-13_14:15:21_result.txt` 和 `2023-08-13_14:15:21_sorted_result.txt`

```shell
# nslookup 默认 timeout 为 5s, 默认 retry 为 3 次
ansible-playbook -i ./inventory.ini ./playbook.yaml --extra-vars "elapsed=3600 interval=3 dns_timeout=5 dns_retry=3"
```
在 `./playbook.yaml` 运行过程中, 也可以使用 `./show_me_now.yaml` 查看结果, 结果同样保存在 `./playbook.yaml` 文件目录下, 形如 `2023-08-13_14:15:21_result.txt` 和 `2023-08-13_14:15:21_sorted_result.txt`


## 查看常用命令

```shell
ansible-playbook -i ./inventory.ini ./show_me_now.yaml

# 排序查看
# 查找无法解析的域名
cat $(ls -t --time=ctime ./*_sorted_result.txt | head -n 1) | grep "can NOT find"
# 查找无法链接的 DNS 服务器
cat $(ls -t --time=ctime ./*_sorted_result.txt | head -n 1) | grep "timed OUT connection to dns"

```

```shell
ansible -i ./inventory.ini all -m shell -a "rm -rf /tmp/cluster_nslookup_v0.2"
```

## `playbook.yaml` 参数说明




## 各文件说明

- `dnss.txt`:
- `domains.txt`:
- `inventory.txt`: 遵循 playbook
- `*_result.txt`: 例如 `2023-08-13_14:15:21_result.txt`
- `*_sorted_result.txt`: 例如 `2023-08-13_14:15:21_sorted_result.txt`
