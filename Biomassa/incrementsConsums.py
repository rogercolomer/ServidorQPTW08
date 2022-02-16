import csv
import os
import mysql.connector
from datetime import datetime
import numpy as np

# Consulta base de dades de incrememtns -> Agafar la ultima dada
# Seleccionar consums mes grans que aquesta data
# Calcular increments
# Guardar incrments

def readLastInc():
    sql = "SELECT * FROM consumsIncrements ORDER BY timestamp DESC Limit 1"
    mydb = mysql.connector.connect(
        host='192.100.101.40',
        user='biomassa',
        passwd='123456789',
        database='biomassa')
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    var = mycursor.fetchall()
    mydb.close()
    return var


def readConsums(date):
    sql = "SELECT * FROM consums WHERE timestamp >'"+date+"'ORDER BY timestamp ASC"
    mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
                database='biomassa')
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    var = mycursor.fetchall()
    mydb.close()
    return var

lastInc = readLastInc()
if lastInc == []:
    dateLastInc = '2022-01-01 00:00:00'
else:
    dateLastInc = lastInc[0][0].strftime("%Y-%m-%d %H:%M:%S")

consums = readConsums(dateLastInc)

superList = []
for v in consums:
    miniList = []
    c = 0
    for d in v:
        if c == 0:
            miniList.append(d)
            c+=1
        else:
            if d is not None:
                miniList.append(float(d))
            c += 1
    superList.append(miniList)
# print(superList[0][1:])

for i in range(len(superList)-1):
    data = np.array(superList[i+1][1:])-np.array(superList[i][1:])
    np.around(data,2)
    # data = np.insert(data,0,str(superList[i][0]),axis=0)
    # dList = data.tolist()
    # dList.pop(8)
    dList = data.tolist()
    indx = 0
    for d in dList:
        dList[indx] = round(d,2)
        indx +=1
    dList.append(superList[i][0])
    print(dList)
    # Falta el consum de aigua i gas
    sql = """INSERT INTO consumsIncrements(TCTR_103_CT_01_ME_ENERGIA, TCTR_103_CT_02_ME_ENERGIA, TCTR_103_CT_05_ME_ENERGIA
            ,TCTR_103_CT_03_ME_ENERGIA, TCTR_103_CT_01_ME_KG_SEG_PCI, TCTR_103_CT_04_ME_ENERGIA, TCTR_103_CT_01_ME_KGH_SEG_PCI,
            timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

    mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
                database='biomassa')
    mycursor = mydb.cursor()
    mycursor.executemany(sql, [tuple(dList)])
    mydb.commit()
    mydb.close()

