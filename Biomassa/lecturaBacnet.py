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
        print(self.taula)
        for e in self.keys:
            self.estatTemp.append(round(data[e]["value"],2))
        print(self.estatTemp)

    def saveDB(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
                database=self.db)
            mycursor = mydb.cursor()
            mycursor.executemany(self.sql, [tuple(self.estatTemp)])
            print(self.estatTemp)
            mydb.commit()
            mydb.close()
            print('done')
            self.deletePastData()
        except:
            print('error save DB ')

    def deletePastData(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
                database=self.db)
            mycursor = mydb.cursor()
            sql = """DELETE FROM """+self.taula+""" WHERE timestamp < '"""+(datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")+"'"
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
            host= '192.100.101.40',
            user= 'biomassa',
            passwd= '123456789',
            database= self.db)
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
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
                database=self.db)
            mycursor = mydb.cursor()
            sql = """INSERT INTO alarmes(timestamp,alarmName,missatge) VALUES(%s,%s,%s)"""
            print([tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyAlarma,self.json["variables"][keyAlarma]])])
            mycursor.executemany(sql, [tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyAlarma,self.json["variables"][keyAlarma]])])
            mydb.commit()
            mydb.close()
            print('done save Alarmes actives')
        except:
            print('error save Alarmes ')

    def deleteAlarm(self,keyAlarma):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
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
        print(self.sql)
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
            print(self.consums)
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='biomassa',
                passwd='123456789',
                database=self.db)
            mycursor = mydb.cursor()
            data = [datetime.now()]
            for i in self.consums:
                data.append(self.consums[i])
            mycursor.executemany(self.sql, [tuple(data)])
            mydb.commit()
            mydb.close()
            print('done save Cosums')
        except:
            print('error save Consums ')


e = estatPlanta(file = "/home/roger/repositori/biomassa/estat.json")
e.getQuery()
f = alarmesBio(file = "/home/roger/repositori/biomassa/alarmes.json")
g = consumsBio(file = "/home/roger/repositori/biomassa/consum.json")
g.getQuery()
# Falten les seguents variables
# "TCTR_100_ME_CONTA_AIGUA",
# "TCTR_100_ME_CONTA_GAS"
t0 = datetime.now()
while(True):
    try:
        lecturaDispositiu('192.100.101.89/23', 100)
        lecturaDispositiu('192.100.101.90/23', 101)
        lecturaDispositiu('192.100.101.91/23', 102)
        lecturaDispositiu('192.100.101.92/23', 103)
        lecturaDispositiu('192.100.101.93/23', 104)
        lecturaDispositiu('192.100.101.94/23', 106)

        e.getValues(values)
        e.saveDB()
        f.getAlarms(values)
        if t0+timedelta(minutes=10) < datetime.now():
            g.getConsums(values)
            t0 = datetime.now()
        time.sleep(10)
    except KeyboardInterrupt:
        raise
    except Exception as ai:
        print(ai)



