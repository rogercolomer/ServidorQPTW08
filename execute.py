import os
import subprocess
from datetime import datetime, timedelta
import time


def estructures():
    '''Estructures'''
    print('estructures')
    os.system('python3 /home/roger/repositori/ServidorQPWood/Estructures/main.py')

def maquinesQPW():
    ''' Totes les maquines connecades a mesboko '''
    print('maquines')
    os.system('python3 /home/roger/repositori/ServidorQPWood/maquinesQPW/main.py')

def servidorMoll():
    '''Programes del servidor moll'''
    print('Server')
    os.system('python3 /home/roger/repositori/ServidorQPWood/ServidorMoll/main.py')

def copyFiles():
    estructures()
    maquinesQPW()
    servidorMoll()

hEstructures = datetime.now()
hMaquinesQPW = datetime.now()
hServidorMoll = datetime.now()
flag_backups = 0

while (True):
    print(flag_backups)
    if datetime.now().weekday() == 0 and datetime.now().hour == 15:
        if flag_backups == 0:
                copyFiles()
                flag_backups = 1
    elif datetime.now().day == 5:
        flag_backups = 0
    time.sleep(10)
