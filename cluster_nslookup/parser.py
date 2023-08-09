#!/bin/python3

import re
import os

hosts_results_dir = '/tmp/serial_nslookup_data/'


class answer:
    def __init__(self):
        self.name = ""
        self.address = ""


class domain:
    def __init__(self):
        self.server = ""
        self.address = ""
        self.answers: [answer] = []
        self.real = ""
        self.user = ""
        self.sys = ""
        self.date = ''


class host_result:
    def __init__(self) -> None:
        self.host_ip = ''
        self.results: [domain] = []

    def print_hr(self) -> None:
        for domain in self.results:
            for answer in domain.answers:
                print(
                    f'{domain.date:<32}{domain.server:<18}{self.host_ip:<18}{answer.name:<28}{answer.address:<18}{domain.real:<10}')


class hosts_results:
    def __init__(self) -> None:
        self.results: [host_result] = []

    def print_hsrs(self) -> None:
        for hr in self.results:
            hr.print_hr()

    def print_table_head(self) -> None:
        answer_name = 'Domain'
        answer_address = 'Address'
        domain_server = 'DNS'
        domain_address = ''
        domain_real = 'Real'
        domain_user = ''
        domain_sys = ''
        domain_date = 'Date'
        host_result_host_ip = 'Source'
        print(
            f'{domain_date:<32}{domain_server:<18}{host_result_host_ip:<18}{answer_name:<28}{answer_address:<18}{domain_real:<10}')


def parse_serial_nslookup_host_result(file_path: str) -> host_result:

    hr = host_result()

    hr.host_ip = re.search(
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', file_path).group()

    with open(file_path) as f:
        line = f.readline()
        while line:
            kv = line.split()
            # print(kv, type(kv))
            if 'Server:' in kv:
                d = domain()
                hr.results.append(d)
                hr.results[-1].server = kv[1]
            elif 'Address:' in kv:
                hr.results[-1].address = kv[1]
            elif 'NXDOMAIN' in kv:
                a = answer()
                hr.results[-1].answers.append(a)
                hr.results[-1].answers[-1].name = kv[4][:-1]
                hr.results[-1].answers[-1].address = kv[5]
            elif 'Name:' in kv:
                a = answer()
                hr.results[-1].answers.append(a)
                hr.results[-1].answers[-1].name = kv[1]
                line = f.readline()
                kv = line.split()
                hr.results[-1].answers[-1].address = kv[1]
            elif 'real' in kv:
                hr.results[-1].real = kv[1]
            elif 'user' in kv:
                hr.results[-1].user = kv[1]
            elif 'sys' in kv:
                hr.results[-1].sys = kv[1]
                line = f.readline()
                hr.results[-1].date = line.strip()
            line = f.readline()
    return hr


def get_all_file_paths(directory: str) -> list:
    file_paths = []  # 存储所有文件的绝对路径

    # 遍历目录及子目录中的所有文件
    for root, directories, files in os.walk(directory):
        for file_name in files:
            # 获取文件的绝对路径
            file_path = os.path.abspath(os.path.join(root, file_name))
            file_paths.append(file_path)

    return file_paths


def parse_hosts_results(host_results_dir: str) -> hosts_results:
    hsrs = hosts_results()
    for serial_nslookup_host_result in get_all_file_paths(hosts_results_dir):
        hsrs.results.append(parse_serial_nslookup_host_result(
            serial_nslookup_host_result))
    return hsrs


hsrs = parse_hosts_results(hosts_results_dir)
hsrs.print_table_head()
hsrs.print_hsrs()
