#!/bin/python3

"""
  需求:
    1. 如果是 APP 类型的虚拟机, 将额外磁盘全部挂载至 /data 目录
    2. 如果是 container 类型的虚拟机
      1. 如果是 ubuntu 20.04, 将额外磁盘对半挂载至 /var/lib/kubelet 和 /var/lib/kubelet
      2. 如果是 centos 7.9, 将额外磁盘对半挂载至 /var/lib/docker 和 /var/lib/kubelet

"""
import fabric
from fabric import Connection


class PhysicalVolume:
    ssh_conn = "conn in pv"
    
    def __init__(self, ssh_conn: fabric.Connection):
        print(self.ssh_conn)
        pass
    
    def _get_info_from_ssh_conn(self, ssh_conn: fabric.Connection):
        pass
    
    def refresh(self):
        pass


if __name__ == '__main__':
    host = '10.0.0.22'
    user = 'root'
    password = 'kjhl'
    
    result = Connection(host, user, connect_kwargs={'password': password}).run('pvdisplay', hide=True)
    PhysicalVolume(Connection(host, user, connect_kwargs={'password': password}))
    print(result.stdout)
