import os
import subprocess
from datetime import datetime, timedelta
import mysql.connector
import time
from pexpect import pxssh


pantalles = {
    "pantalla1" : {"ip":"147.45.45.250","user":"pi","pwd":"123456789"},
    "pantalla2" : {"ip":"147.45.45.251","user":"pi","pwd":"123456789"},
    "pantalla3" : {"ip":"147.45.45.252","user":"pi","pwd":"123456789"},
    "pantalla4" : {"ip":"147.45.45.253","user":"pi","pwd":"123456789"},
    "fishTank"  : {"ip":"147.45.44.206","user":"pi","pwd":"123456789"},
}
for p in pantalles:
    try:
        print(pantalles[p]["ip"])
        s = pxssh.pxssh(timeout=10)
        s.login(pantalles[p]["ip"], pantalles[p]["user"], pantalles[p]["pwd"])
        s.sendline('sudo reboot')
        s.logout()
    except Exception as e:
        print(e)