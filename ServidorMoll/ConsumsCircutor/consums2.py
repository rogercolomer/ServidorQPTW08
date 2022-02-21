import requests
import time
import mysql.connector
from datetime import datetime
from statistics import mean
import json
import xmltodict

def getConsums():

    urls = ['http://147.45.45.3:22222/services/user/values.xml?var=General.API?...?id=General?...']
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
    return valorConsum
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





