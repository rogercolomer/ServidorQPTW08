import paramiko
import time
import json
import mysql.connector
from paramiko import *
from scp import SCPClient
from pexpect import pxssh
from datetime import datetime, timedelta
from subprocess import check_output, run

file = open('/home/roger/repositori/ServidorQPWood/Estructures/lines.json')
lines = json.load(file)
file.close()

for l in lines:
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    print(l,lines[l]["ip"][0],22,lines[l]["user"],lines[l]["pwd"])
    ssh.connect(lines[l]["ip"][0],22,lines[l]["user"],lines[l]["pwd"])
    if lines[l]["device"] == "IOT2040" or lines[l]["device"] == "IOT2050":
        print(l)
        if l != 'BackupsRobots' and l != 'Seccionadors' and l != 'sirenaHoraria':
            path = "/home/root/"
        else:
            path = "/home/root/"+l+"/"
    else:
        path = "/home/pi/"
    stdin, stdout, stderr = ssh.exec_command('cd '+path+';ls')
    files = bytes(stdout.read()).decode("utf-8")
    allF = files.split('\n')

    scp = SCPClient(ssh.get_transport())
    print(path)
    for f in allF:
        if f != '' and (f.find('.py') != -1 or f.find('.json') != -1):
            print(f)
            if l != 'BackupsRobots' or l != 'Seccionadors' or l != 'sirenaHoraria':
                print(path+f,'/home/roger/repositori/ServidorQPWood/Estructures/'+l)
                scp.get(path+f,'/home/roger/repositori/ServidorQPWood/Estructures/'+l)
            else:
                print(path+l+'/'+f, '/home/roger/repositori/ServidorQPWood/Estructures/' + l)
                scp.get(path+l+'/'+f, '/home/roger/repositori/ServidorQPWood/Estructures/' + l)

    scp.close()
