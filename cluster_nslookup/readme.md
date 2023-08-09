## cluster_nslookup

a tool for querying DNS records on hosts in a cluster.

## Role of Important File

- `playbook.yaml`: describing the execution process
- `serial_nslookup.sh`: generating DNS resolution data `/tmp/ansible/serial_nslookup_host_result.txt` on each host in cluster
- `parser.py`: parsing the collected data `/tmp/serial_nslookup_data/` to the file `./cluster_nslookup/result.txt`
- `domains.txt`: domains that require DNS resolution on each host in the cluster
- `inventory.ini`: list of host to be operated in the cluster
- `result.txt`: final result 

## How to Use

```shell
rm -rf ./result.txt && ansible-playbook -i ./inventory.ini ./playbook.yaml
cat ./result.txt
```


## FAQ(Frequently Asked Questions)

### 未安装 nslookup

**Handling Method**

```shell
yum install bind-utils
```