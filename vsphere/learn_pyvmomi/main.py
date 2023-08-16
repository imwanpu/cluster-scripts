#!/usr/bin/env python3

import ssl

from pyVmomi import vim
from pyVim.connect import SmartConnect
from pyVim.task import WaitForTask


def Conn(
    host='10.223.129.102',
    user='administrator@vsphere.local',
    pwd='Admin123@+',
):

    # 取消 ssl 验证
    ssl_content = ssl.SSLContext()
    ssl_content.check_hostname = False
    ssl_content.verify_mode = ssl.CERT_NONE

    # 获取链接
    vm_ins = SmartConnect(
        host=host, user=user, pwd=pwd, sslContext=ssl_content)
    # 获取上下文
    content = vm_ins.RetrieveContent()
    # 获取根路径容器
    container = content.rootFolder
    # 指定vim类型
    vm_type = [vim.VirtualMachine]
    recursive = True
    # 回去容器视图，这里面装的就是所有的VirtualMachine虚机
    containerView = content.viewManager.CreateContainerView(
        container, vm_type, recursive)
    # 将虚机容器返回
    return containerView

# 根据名称找虚机对象


def getVmbyName(name):
    vms = Conn()
    for i in vms.view:
        if i.name == name:
            print(i, i.name)
            return i


if __name__ == '__main__':
    ds = Conn()
    for i in ds.view:
        print(i.name, i.runtime.powerState)
