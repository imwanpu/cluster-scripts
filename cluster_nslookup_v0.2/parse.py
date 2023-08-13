#!/bin/python3

import re
import os
import sys
import subprocess
import datetime

collected = f'{os.path.dirname(os.path.abspath(__file__))}/collected_data'
result_dir = f'{os.path.dirname(os.path.abspath(__file__))}/'


class answer:
    def __init__(self):
        self.name = ''
        self.address = ''
        self.explanation = ''


class domain_line:
    def __init__(self, result_line: str):
        self.server = ''
        self.address = ''
        self.answers: [answer] = []
        self.real = ''
        self.user = ''
        self.sys = ''
        self.date = ''

        split_n = result_line.split('@@@')
        iterator = iter(split_n)
        line = next(iterator)
        self.date = line.strip()

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
                    a.explanation = 'timed OUT connection to dns'
                    self.answers.append(a)
                elif '''** server can't find''' in striped_line:
                    a = answer()
                    a.explanation = 'can NOT find'
                    self.answers.append(a)
                elif 'arg_domain:' in striped_line:
                    self.answers[-1].name = striped_line.split()[1]
                elif 'arg_dns:' in striped_line:
                    self.server = striped_line.split()[1]
                elif 'Name:' in striped_line:
                    a = answer()
                    a.name = striped_line.split()[1]
                    line = next(iterator)
                    a.address = line.strip().split()[1]
                    a.explanation = 'can find'
                    self.answers.append(a)
                elif 'real' in striped_line:
                    self.real = striped_line.split()[1]
                elif 'user' in striped_line:
                    self.user = striped_line.split()[1]
                elif 'sys' in striped_line:
                    self.sys = striped_line.split()[1]

            except StopIteration:
                break


class host_result:
    def __init__(self, result_path) -> None:
        self.host_ip = ''
        self.results: [domain_line] = []

        self.host_ip = re.search(
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', result_path).group()
        with open(result_path) as f:
            line = f.readline()
            while line:
                dl = domain_line(line.strip())
                self.results.append(dl)
                line = f.readline()


class hosts_results:

    def __get_all_file_paths(self, directory: str) -> list:
        file_paths = []  # 存储所有文件的绝对路径

        # 遍历目录及子目录中的所有文件
        for root, directories, files in os.walk(directory):
            for file_name in files:
                # 获取文件的绝对路径
                file_path = os.path.abspath(os.path.join(root, file_name))
                file_paths.append(file_path)

        return file_paths

    def __init__(self, resutl_dir) -> None:

        self.date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.hsrs: [host_result] = []

        for result_file in self.__get_all_file_paths(collected):
            hr = host_result(result_file)
            self.hsrs.append(hr)

    def __write_title2file(self, result_file):
        host_result_ip = 'Host IP'
        domain_server = 'DNS Server'
        domain_address = ''
        answer_name = 'Domain Name'
        answer_address = 'Domain Address'
        answer_explanation = 'Explanation'
        domain_real = 'real'
        domain_user = 'user'
        domain_sys = 'sys'
        domain_date = 'Date'

        with open(result_file, 'w') as f:
            f.write(f'{domain_date:<19}\t'
                    f'{host_result_ip:<15}\t'
                    f'{domain_server:<15}\t'
                    f'{answer_name:<25}\t'
                    f'{answer_address:<15}\t'
                    f'{answer_explanation:<27}\t'
                    f'{domain_real:<8}\t'
                    f'{domain_user:<8}\t'
                    f'{domain_sys:<8}\n')

    def __write_hsrs2file(self, result_file):
        with open(result_file, 'a') as f:
            for hr in self.hsrs:
                for dl in hr.results:
                    for a in dl.answers:
                        #     f.write(f'{dl.date:<19}\t'
                        #             f'{hr.host_ip}'
                        #             f'\n')
                        f.write(f'{dl.date:<19}\t'
                                f'{hr.host_ip:<15}\t'
                                f'{dl.server:<15}\t'
                                f'{a.name:<25}\t'
                                f'{a.address:<15}\t'
                                f'{a.explanation:<27}\t'
                                f'{dl.real:<8}\t'
                                f'{dl.user:<8}\t'
                                f'{dl.sys:<8}\n')

    def write2file(self, result_dir):
        result_file = f'{result_dir}{self.date}_result.txt'
        self.__write_title2file(result_file)
        self.__write_hsrs2file(result_file)

        sorted_result_file = f'{result_dir}{self.date}_sorted_result.txt'
        command = f'tail -n +2 {result_file} | sort -k1 -k2 -k3 > {sorted_result_file}'
        subprocess.run(command, shell=True)
        print(result_file)
        print(sorted_result_file)


hsrs = hosts_results(collected)
hsrs.write2file(result_dir)
