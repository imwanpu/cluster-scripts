#!/bin/python3


import subprocess
import multiprocessing
import time


def ssh_run_passwordless(host: str, command: str):
    # 传入一个函数操作结果,

    ssh_command = f'''ssh -o stricthostkeychecking=no {host} "{command}"'''
    result = subprocess.run(ssh_command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding='utf-8'
                            )
    print(result)


if __name__ == '__main__':
    command = 'date && hostname && sleep 3'
    args_o = [('10.0.0.21', command), ('10.0.0.22', command), ('10.0.0.23', command)]
    args = args_o * 100
    pool = multiprocessing.Pool(processes=18)
    results = pool.starmap(ssh_run_passwordless, args)
    pool.close()
    pool.join()
