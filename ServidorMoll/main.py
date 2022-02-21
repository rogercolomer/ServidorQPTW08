import paramiko
import time
import json
import mysql.connector
from paramiko import *
from scp import SCPClient
from pexpect import pxssh
from datetime import datetime, timedelta
from subprocess import check_output, run

file = open('/home/roger/repositori/ServidorQPWood/ServidorMoll/scrip.json')
lines = json.load(file)
file.close()
print(lines)

for l in lines:
    print(l)
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect('192.100.101.40',22,'root','123456789')
    if lines[l] == ['*']:
        stdin, stdout, stderr = ssh.exec_command('cd /home/server/'+l+';ls')
        files = bytes(stdout.read()).decode("utf-8")
        allF = files.split('\n')
    else:
        allF = lines[l]
    scp = SCPClient(ssh.get_transport())
    print(allF)
    for f in allF:
        if f != '':
            print('/home/server/'+l+'/'+f,'/home/roger/repositori/ServidorQPWood/ServidorMoll/'+l+'/')
            scp.get('/home/server/'+l+'/'+f,'/home/roger/repositori/ServidorQPWood/ServidorMoll/'+l+'/')
    scp.close()
