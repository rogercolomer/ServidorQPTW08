import time
import numpy as np
import mysql.connector
import json
import snap7.client as c
from snap7.util import *
from datetime import datetime
from time import sleep

sleep(30)

def readSeccionadors(plc):
    plc.connect('192.100.101.33', 0, 1)
    data = plc.db_read(2, 0, 22)     # llegir db (numero_db,primer byte, longitud maxima)
    val = []
    print(data)
    for i in range(0,22,2):
        val.append(int.from_bytes(data[i:i+2], "big"))
    print(val)
    plc.disconnect()
    return val

def saveState(estat):
    sql = """INSERT INTO SeccionadorsGenerals(timestamp, 1A, 1B, Biomassa, Compressors, 2A, 2B, 2C, Magatzem, OTR_Pintura, Aspiracio, DiferencialSAI) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    mydb = mysql.connector.connect(
        host='192.100.101.40',
        user='consums',
        passwd='123456789',
        database='consums')
    mycursor = mydb.cursor()
    mycursor.executemany(sql, [(datetime.now(),estat[0], estat[1], estat[2], estat[3], estat[4], estat[5], estat[6], estat[7], estat[8], estat[9], estat[10])])
    mydb.commit()
    mydb.close()

def deleteState():
    sql = """SELECT * FROM SeccionadorsGenerals ORDER BY timestamp DESC LIMIT 2"""
    mydb = mysql.connector.connect(
        host='192.100.101.40',
        user='consums',
        passwd='123456789',
        database='consums')
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    var = mycursor.fetchall()
    sql = "DELETE FROM SeccionadorsGenerals WHERE timestamp<'"+str(var[1][0])+"'"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


plc = c.Client()
estatAnterior = readSeccionadors(plc)
alarmaActiva = 0
while True:
    # try:
    estatActual = readSeccionadors(plc)
    difEstats = []
    for i in range(len(estatAnterior)):
        difEstats.append(estatAnterior[i]-estatActual[i])
    difArr = np.array(difEstats)
    print(estatAnterior,estatActual,difArr)
    if np.any(difArr != 0) :
        saveState(difEstats)
        alarmaActiva = 1
        deleteState()
    if np.all(estatActual == 0) and alarmaActiva == 1:
        saveState(estatActual)
        alarmaActiva = 0
        deleteState()
    estatAnterior = estatActual
    sleep(10)
    # except:
    #     print('error')
    #     sleep(10)

