import time
import BAC0
import mysql.connector
from datetime import datetime, timedelta
import json
import os


bacnet = BAC0.lite()
values ={}

def lecturaDispositiu(ip,deviceID):
    try:
        dev = BAC0.device(ip, deviceID, bacnet, poll=30)
        var = dev.points
        for v in var:
            values[v.properties.name] = {}
            values[v.properties.name]["value"] = v.lastValue
            values[v.properties.name]["description"] = v.properties.description
            values[v.properties.name]["type"] = v.properties.type
    except:
        pass


class estatPlanta():
    def __init__(self, file):
        self.file = file
        self.json = self.getKeys()
        self.keys = self.json["variables"]
        self.db = self.json["db"]
        self.taula = self.json["taula"]

    def getQuery(self):
        sql = "INSERT INTO "+self.taula+"(timestamp,"
        sql1 = ") VALUES (%s,"
        for k in self.keys:
            pGuio = k.find('-')
            pPunt = k.find('.')
            if pGuio != -1:
                k = k.replace('-','_')
            if pPunt != -1:
                k = k.replace('.','_')
            sql += k + ','
            sql1 += '%s,'
        self.sql =  sql[:-1] + sql1[:-1] + ')'

    def getKeys(self):
        file = open(self.file)
        dicConfig = json.load(file)
        file.close()
        return dicConfig

    def getValues(self,data):
        self.estatTemp = [datetime.now()]
        for e in self.keys:
            if data[e]["value"] == "active":
                self.estatTemp.append(1)
            elif data[e]["value"] == "inactive":
                self.estatTemp.append(0)
            else:
                self.estatTemp.append(float(round(data[e]["value"],2)))

    def saveDB(self):
        try:
            mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
            mycursor = mydb.cursor()
            print(self.estatTemp)
            mycursor.executemany(self.sql, [tuple(self.estatTemp)])
            mydb.commit()
            mydb.close()
            print('done')
            self.deletePastData()
        except:
            print('error save DB ')

    def deletePastData(self):
        try:
            if self.db != 'predictiu_aspiracio':
                mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
                mycursor = mydb.cursor()
                sql = """DELETE FROM """ + self.taula + """ WHERE timestamp < '""" + (
                        datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S") + "'"
                print(sql)
                mycursor.execute(sql)
                mydb.commit()
                mydb.close()
        except:
            print("error delete DB")


class alarmesBio(estatPlanta):
    def __init__(self,file):
        super().__init__(file)

    def getAlarms(self,data):
        alarmesActives = {}
        for i in self.json["variables"]:
            if data[i]["value"] != 'inactive':
                alarmesActives[i] = self.json["variables"][i]
        mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
        mycursor = mydb.cursor()
        sql = """SELECT * FROM alarmes """
        mycursor.execute(sql)
        var = mycursor.fetchall()
        # Alarmes de la DB en un JSON
        alarmesDB = {}
        for v in var:
            alarmesDB[v[1]] = v[2]
        mydb.close()
        #Compraracio de les alarmes escrites a la DB i les llegides per el bacnet
        for k in alarmesActives:
            if k in alarmesDB:
                print(alarmesActives[k])
                del alarmesDB[k]
            else:
                self.saveAlarm(k)
        for i in alarmesDB:
            self.deleteAlarm(i)

    def saveAlarm(self,keyAlarma):
        try:
            mydb = mysql.connector.connect(
                host='x.x.x.x',
                user='xxxxx',
                passwd='xxxx',
                database=self.db)
            mycursor = mydb.cursor()
            sql = """INSERT INTO alarmes(timestamp,alarmName,missatge,alarmValue) VALUES(%s,%s,%s,%s)"""
            print([tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyAlarma,self.json["variables"][keyAlarma]])])
            mycursor.executemany(sql, [tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyAlarma,self.json["variables"][keyAlarma]["message"],self.json["variables"][keyAlarma]["value"]])])
            mydb.commit()
            mydb.close()
            print('done save Alarmes actives')
        except:
            print('error save Alarmes ')

    def deleteAlarm(self,keyAlarma):
        try:
            mydb = mysql.connector.connect(
                host='x.x.x.x',
                user='xxxxx',
                passwd='xxxx',
                database=self.db)
            mycursor = mydb.cursor()
            sql = "DELETE FROM alarmes WHERE alarmName='"+keyAlarma+"'"
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
            print('done Delete Alarmes mariaDB')
        except:
            print('error delete Alarmes ')

class consumsBio(estatPlanta):
    def __init__(self,file):
        super().__init__(file)

    def getConsums(self,data):
        self.consums = {}
        for i in self.json["variables"]:
            try:
                self.consums[i] = data[i]["value"]
                print(i, data[i]["value"])
            except:
                print("error",i)
        self.saveConsum()

    def saveConsum(self):
        try:
            print('consums',self.consums)
            mydb = mysql.connector.connect(
                host='x.x.x.x',
                user='xxxx',
                passwd='xxxx',
                database=self.db)
            mycursor = mydb.cursor()
            data = [datetime.now()]
            for i in self.consums:
                data.append(float(round(self.consums[i],2)))
            mycursor.executemany(self.sql, [tuple(data)])
            mydb.commit()
            mydb.close()
            print('done save Cosums')
        except:
            print('error save Consums ')

class tempHumiBio(estatPlanta):
    def __init__(self,file):
        super().__init__(file)

    def getConsums(self,data):
        self.consums = {}
        for i in self.json["variables"]:
            try:
                self.consums[i] = data[i]["value"]
                print(i, data[i]["value"])
            except:
                print("error",i)
        self.saveConsum()

    def saveConsum(self):
        try:
            print('consums',self.consums)
            mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
            mycursor = mydb.cursor()
            data = [datetime.now()]
            for i in self.consums:
                data.append(float(round(self.consums[i],2)))
            mycursor.executemany(self.sql, [tuple(data)])
            mydb.commit()
            mydb.close()
            print('done save Cosums')
        except:
            print('error save Consums ')

e = estatPlanta(file = "/home/roger/repositori/ServidorQPWood/Biomassa/estat.json")
e.getQuery()
f = alarmesBio(file = "/home/roger/repositori/ServidorQPWood/Biomassa/alarmes.json")
g = consumsBio(file = "/home/roger/repositori/ServidorQPWood/Biomassa/consum.json")
g.getQuery()
h = estatPlanta(file = "/home/roger/repositori/ServidorQPWood/Biomassa/temperatures.json")
h.getQuery()
# Falten les seguents variables
# "TCTR_100_ME_CONTA_AIGUA",
# "TCTR_100_ME_CONTA_GAS"
t0 = datetime.now()
minAnterior = datetime.now().minute
while(True):
    try:
        lecturaDispositiu(x.x.x.x, X)
        lecturaDispositiu(x.x.x.x, X)
        lecturaDispositiu(x.x.x.x', X)
        lecturaDispositiu(x.x.x.x, X)
        lecturaDispositiu(x.x.x.x, X)
        lecturaDispositiu(x.x.x.x, X)

        e.getValues(values)
        e.saveDB()
        f.getAlarms(values)
        if t0+timedelta(minutes=15) < datetime.now():
            g.getConsums(values)
            t0 = datetime.now()
        if minAnterior != datetime.now().minute:
            h.getValues(values)
            h.estatTemp[0] = datetime.now().replace(second=0,microsecond=0)
            h.saveDB()
            minAnterior =datetime.now().minute

        time.sleep(10)
    except KeyboardInterrupt:
        raise
    except Exception as ai:
        print(ai)



