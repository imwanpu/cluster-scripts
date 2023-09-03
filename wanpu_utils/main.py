#!/bin/python3

"""
usage: 在远程 Linux 主机上并发执行命令, 并收集结果

WARNING: 不考虑 windows 支持, 进支持 CentOS 7.9 Ubuntu 20.04 等 Linux 系统

"""

import subprocess
import os
import multiprocessing
from functools import partial

from typing import List, Callable


def ssh_run_passwordless(host: str,
                         command: str,
                         hook: Callable[[subprocess.CompletedProcess, ], None] = None
                         ) -> None:
    ssh_command = f'''ssh -o stricthostkeychecking=no {host} "{command}"'''
    hook(subprocess.run(ssh_command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8'
                        ))


def run_command2hosts(
        hosts: List[str],
        command: str,
        processes: int = multiprocessing.cpu_count() * 2,
        hook: Callable[[subprocess.CompletedProcess, ], None] = None
) -> None:
    pool = multiprocessing.Pool(processes)
    pool.map(partial(ssh_run_passwordless, command=command, hook=hook), hosts)
    pool.close()
    pool.join()


if __name__ == '__main__':
    hosts = ['10.0.0.21', '10.0.0.22', '10.0.0.23'] * 10
    command = 'date && time nslookup baidu.com 114.114.114.114'
    hook = print
    run_command2hosts(hosts, command, processes=3,hook=hook)
