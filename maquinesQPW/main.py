from subprocess import check_output, run

import paramiko
from pexpect import pxssh
from datetime import datetime, timedelta
import time
import json
import mysql.connector
from paramiko import *
from scp import SCPClient

dicMeta = {}
file = open('/home/roger/repositori/ServidorQPWood/maquinesQPW/lines.json')
lines = json.load(file)
file.close()
print(lines)

# for l in lines:
''''https://www.programcreek.com/python/example/4561/paramiko.SSHClient'''
for l in lines:
    if lines[l]['system'] == 'mes':
        try:
            ssh = SSHClient()
            print(ssh.load_system_host_keys())
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(lines[l]["ip"],22,lines[l]["user"],lines[l]["password"])
            # print('/home/server/comprovacioIOT/backupScrips/'+'CadenaPlana')
            # SCPCLient takes a paramiko transport as an argument
            scp = SCPClient(ssh.get_transport())
            scp.get('/home/root/main.py','/home/roger/repositori/ServidorQPWood/maquinesQPW/'+lines[l]["name"])
            scp.get('/home/root/managerDB.py', '/home/roger/repositori/ServidorQPWood/maquinesQPW/'+lines[l]["name"])
            scp.get('/home/root/machineIOT.py', '/home/roger/repositori/ServidorQPWood/maquinesQPW/'+lines[l]["name"])
            scp.get('/home/root/config.json', '/home/roger/repositori/ServidorQPWood/maquinesQPW/'+lines[l]["name"])
            scp.close()
            print("DONE: "+lines[l]['name'])
        except Exception as e:
            print("Fail: " + lines[l]['name'], e)
