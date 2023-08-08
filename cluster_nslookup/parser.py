#!/bin/python3

file_path = '/root/cluster-scripts/cluster_nslookup/serial_nslookup_tmp.txt'

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

class remote_result:
    def __init__(self) -> None:
        self.host_ip = ''
        self.result: [domain] = []

result: [domain] = []

# TODO 抽 function
with open(file_path) as f:
    line = f.readline()
    while line:
        kv = line.split()
        print(kv, type(kv))
        if 'Server:' in kv:
            d = domain()
            result.append(d)
            result[-1].server = kv[1]
        elif 'Address:' in kv:
            result[-1].address = kv[1]
        elif 'Name:' in kv:
            a = answer()
            result[-1].answers.append(a)
            result[-1].answers[-1].name = kv[1]
            line = f.readline()
            kv = line.split()
            result[-1].answers[-1].address = kv[1]
        elif 'real' in kv:
            result[-1].real = kv[1]
        elif 'user' in kv:
            result[-1].user = kv[1]
        elif 'sys' in kv:
            result[-1].sys = kv[1]
            line = f.readline()
            result[-1].date = line.strip()
        line = f.readline()
  
print(result)

print(f'date\t')