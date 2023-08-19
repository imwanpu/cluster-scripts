#!/bin/python3
# -*- coding: utf-8 -*-
#
#
# 在集群中使用 nslookup 并收集信息
#
#

import os
import subprocess
import time
from fabric import Connection, task, Config
from fabric.group import ThreadingGroup

# TODO 参数, 处理传入
command_timeout = '1'
command_retry = '1'
command_elapsed = '10'
command_interval = '3'  # WARNING interval 最好大于 (timeout * retry) + 1


work_dir = os.path.dirname(os.path.abspath(__file__))
# TODO WARNING 写进 readme: 最后留空一行, 下两个文件同
inventory_path = f'{work_dir}/inventory.txt'
domains_path = f'{work_dir}/domains.txt'
dnss_path = f'{work_dir}/dnss.txt'
result_path = f'{work_dir}/result.txt'
sorted_result_path = f'{work_dir}/sorted_result.txt'
db_path = ''  # TODO 写入到db


def file2array(inventory_path) -> [str]:
    arr: [str] = []
    with open(inventory_path) as f:
        line = f.readline()
        while line:
            arr.append(line.strip())
            line = f.readline()
    return arr


hosts: [str] = file2array(inventory_path)
group = ThreadingGroup(*hosts)
domains = file2array(domains_path)
dnss = file2array(dnss_path)


# 解析每次执行结果到对象



class answer:
    def __init__(self):
        self.name = ''
        self.address = ''
        self.explanation = ''


class result_on_host:
    def __init__(self):
        self.ip = ''
        self.server = ''
        self.address = ''
        self.answers: [answer] = []
        self.real = ''
        self.user = ''
        self.sys = ''
        self.date = ''

    def parse_stdout(self, stdout: str):
        split_n = stdout.split('\n')
        self.date = split_n[0].strip()
        iterator = iter(split_n)

        while True:
            try:
                line = next(iterator)
                striped_line = line.strip()
                if 'Server:' in striped_line:
                    self.server = striped_line.split()[1]
                elif 'Address:' in striped_line:
                    self.address = striped_line.split()[1]
                elif ''';; connection timed out;''' in striped_line:
                    a = answer()
                    a.explanation = striped_line
                    self.answers.append(a)
                elif '''** server can't find''' in striped_line:
                    a = answer()
                    a.explanation = striped_line
                    self.answers.append(a)
                elif 'Name:' in striped_line:
                    a = answer()
                    a.name = striped_line.split()[1]
                    line = next(iterator)
                    a.address = line.strip().split()[1]
                    self.answers.append(a)
            except StopIteration:
                break


    def parse_stderr(self, stderr: str):
        split_n = stderr.split('\n')
        for line in split_n:
            split_line = line.strip()
            if 'real' in split_line:
                self.real = split_line.split()[1]
            elif 'user' in split_line:
                self.user = split_line.split()[1]
            elif 'sys' in split_line:
                self.sys = split_line.split()[1]


class result_on_group:
    def __init__(self):
        self.results[result_on_host] = []
        self.command = ''
    def get_result(self, dns, domain, command_timeout=command_timeout)


def sort_result(result_path, sort_result):
    subprocess.run('sort -k1')  # TODO 得到result.txt 之后再整 20s 执行一次?




def start(
    dnss=dnss,
    domains=domains,
    hosts=hosts,
    result_path=result_path,
    sorted_result_path=sorted_result_path,
    db_path=db_path
):
    pass



group_results = group.run(command, hide=True, warn=True)


for conn, host_result in group_results.items():
    roh = result_on_host()
    roh.ip = conn.host
    roh.parse_stdout(host_result.stdout)
    roh.parse_stderr(host_result.stderr)
    print(f'{conn.host}--{host_result.stdout}--{host_result.stderr}')
print('hh')

for dns in dnss:
    for domain in domains:
        command = f'date +%Y-%m-%d_%H:%M:%S && time nslookup -timeout={command_timeout} -retry={command_retry} {domain} {dns}'

    time.sleep(command_interval)