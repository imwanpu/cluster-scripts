#!/bin/python3

import subprocess


def ssh_run_passwordless(host: str, command: str) -> subprocess.CompletedProcess:
    # 传入一个函数操作结果,

    ssh_command = f'''ssh -o stricthostkeychecking=no {host} "{command}"'''
    return subprocess.run(ssh_command,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          encoding='utf-8'
                          )



if __name__ == '__main__':
    command = 'time nslookup baidu.com 114.114.114.114 && hostname'
    host = 'h21'

    result = ssh_run_passwordless(host, command)

    print('hello')
    print('_____________error↓_____________')
    print(result.stderr)
    print('____________stdio↓______________')
    print(result.stdout)
    print('__________________________')


