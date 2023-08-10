from fabric import Connection, task, Config
from fabric.group import ThreadingGroup
import os

inventory_path = f'{os.path.dirname(os.path.abspath(__file__))}/inventory.txt'


def get_group_from_file(file_path: str) -> ThreadingGroup:
    hosts_ips: [str] = []
    with open(file_path) as f:
        line = f.readline()
        while line:
            c = line.strip()
            hosts_ips.append(c)
            line = f.readline()
    return ThreadingGroup(*hosts_ips)


g = get_group_from_file(inventory_path)
results = g.run(
    'date +%Y-%m-%d_%H:%M:%S && time nslookup baidu.com 114.114.114.114', hide=True)
for connection, result in results.items():
    print(f'{connection.host}---{result.stdout}---{result.stderr}')
