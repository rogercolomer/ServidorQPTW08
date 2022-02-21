import os
import subprocess
from datetime import datetime, timedelta
import time


def estructures():
    '''Monitoritzar el WS per verure si funciona correctament, guardant dades al mariaDB'''
    os.system('python3 /home/server/controlWS/estatWS.py &')

def maquinesQPW():
    ''' Llegir i guardar els consums de tota la fabrica en la DB del linux i grafana '''
    os.system('python3 /home/server/consumsCircutor.py &')

def servidorMoll():
    os.system('python3 /home/server/ConsumsCircutor/consumsQuartHoraris.py &')

def copyFiles():
    estructures()
    maquinesQPW()
    servidorMoll()

hEstructures = datetime.now()
hMaquinesQPW = datetime.now()
hServidorMoll = datetime.now()
flag_backups = 0

while (True):
    if datetime.now().weekday() == 4:
        if flag_backups == 0:
                copyFiles()
                flag_backups = 1
    elif datetime.now().day == 5:
        flag_backups = 0
