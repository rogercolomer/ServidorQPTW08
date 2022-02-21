import requests
import time
import json
import xmltodict
import mysql.connector
from datetime import datetime
from statistics import mean


# def getConsums():
#     try:
#         urls = ['http://147.45.45.3:22222/services/user/values.xml?var=General.API?...?id=General?...']
#         n = 0
#         for url in urls:
#             s = requests.Session()
#             data = s.get(url).text
#             api = data.find('API') + 15
#             val = ''
#             for i in range(5):
#                 val += data[api + i]
#             n += 1
#             s.close()
#         return val
#     except:
#         return None

def getConsums():
    try:
        urls = ['http://147.45.45.3:22222/services/user/values.xml?var=General.API?...?id=General?...']
        valorConsum = 0
        for url in urls:
            s = requests.Session()
            data = s.get(url).text
            dataDict = xmltodict.parse(data)
            dataStr = json.dumps(dataDict)
            jD = json.loads(dataStr)
            for j in jD['values']['variable']:
                if j['id'].split('.')[1] == 'API':
                    valorConsum = float(j['value'])
                    break
            s.close()
            print(valorConsum)
        return valorConsum
    except:
        return None

def getPeriode():
    try:
        dataHora = datetime.now()
        mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='consums',
                passwd='123456789',
                database='consums')

        mycursor = mydb.cursor()
        sql = """SELECT mes,hora,tarifa from periode WHERE mes="""+str(dataHora.month)+""" AND hora="""+str(dataHora.hour)
        mycursor.execute(sql)
        var = mycursor.fetchall()
        mydb.close()
        return var[0][2]
    except:
        return None


def getTarifa(periode):
    try:
        mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='consums',
                passwd='123456789',
                database='consums')

        mycursor = mydb.cursor()
        sql = """SELECT periode,consumMax from tarifa WHERE periode="""+str(periode)
        mycursor.execute(sql)
        var = mycursor.fetchall()
        mydb.close()
        return var[0][1]
    except:
        return None

def saveConsums(consum, periode, tarifaMax):
    try:
        exces = float(consum)-float(tarifaMax)
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='consums',
            passwd='123456789',
            database='consums')

        mycursor = mydb.cursor()
        sql = """INSERT INTO tarifaQuarthoraria (timestamp,consum,periode,maxConsum,exces) VALUE (%s,%s,%s,%s,%s)"""
        mycursor.executemany(sql, [tuple([datetime.now(),consum,periode,tarifaMax,exces])])
        mydb.commit()
        mycursor.close()
        mydb.close()
    except:
        pass



print(getConsums(),getPeriode())
quartHorari = 0
periode = 0
listConsums = []
tarifaMax = 0

while True:
    try:
        if datetime.now().minute >= 0 and datetime.now().minute < 15:
            if quartHorari != 1:
                if listConsums != []:
                    consum = mean(listConsums)
                    saveConsums(consum, periode, tarifaMax)
                listConsums = []
                quartHorari = 1
                periode = getPeriode()
                while periode == None:
                    periode = getPeriode()
                    time.sleep(2)
                tarifaMax = getTarifa(periode)
                while tarifaMax == None:
                    tarifaMax = getTarifa()
                    time.sleep(2)
            else:
                try:
                    consumInst = getConsums()
                    if consumInst != None:
                        listConsums.append(float(consumInst))
                    else:
                        pass
                except:
                    pass
        elif datetime.now().minute >= 15 and datetime.now().minute < 30:
            if quartHorari != 2:
                if listConsums != []:
                    consum = mean(listConsums)
                    saveConsums(consum, periode, tarifaMax)
                listConsums = []
                quartHorari = 2
                periode = getPeriode()
                while periode == None:
                    periode = getPeriode()
                    time.sleep(2)
                tarifaMax = getTarifa(periode)
                while tarifaMax == None:
                    tarifaMax = getTarifa()
                    time.sleep(2)
            else:
                try:
                    consumInst = getConsums()
                    if consumInst != None:
                        listConsums.append(float(consumInst))
                    else:
                        pass
                except:
                    pass
        elif datetime.now().minute >= 30 and datetime.now().minute < 45:
            if quartHorari != 3:
                if listConsums != []:
                    consum = mean(listConsums)
                    saveConsums(consum, periode, tarifaMax)
                listConsums = []
                quartHorari = 3
                periode = getPeriode()
                while periode == None:
                    periode = getPeriode()
                    time.sleep(2)
                tarifaMax = getTarifa(periode)
                while tarifaMax == None:
                    tarifaMax = getTarifa()
                    time.sleep(2)
            else:
                try:
                    consumInst = getConsums()
                    if consumInst != None:
                        listConsums.append(float(consumInst))
                    else:
                        pass
                except:
                    pass
        elif datetime.now().minute >= 45 and datetime.now().minute <= 59:
            if quartHorari != 4:
                if listConsums != []:
                    consum = mean(listConsums)
                    saveConsums(consum, periode, tarifaMax)
                listConsums = []
                quartHorari = 4
                periode = getPeriode()
                while periode == None:
                    periode = getPeriode()
                    time.sleep(2)
                tarifaMax = getTarifa(periode)
                while tarifaMax == None:
                    tarifaMax = getTarifa()
                    time.sleep(2)
            else:
                try:
                    consumInst = getConsums()
                    if consumInst != None:
                        listConsums.append(float(consumInst))
                    else:
                        pass
                except:
                    pass
        time.sleep(1)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(e)



