import time
import mysql.connector
import serial
import json
import snap7.client as c
from datetime import datetime
from snap7.util import *
from snap7.snap7types import *


class Values:

    def __init__(self,v):
        self.values = []
        self.alarmes = []
        self.alarmCode =[]
        self.file = '/home/root/alarmes.json'
        self.sql_values = self.create_query('value',v)
        self.sql_data = self.create_query('data', v)
        self.alarmsJson = self.getKeys()

    def get_values(self):
        return self.values

    def get_alarmes(self):
        return self.alarmes

    def read_variables(self):
        try:
            values = [datetime.now()]
            alarmes = [datetime.now()]
            plc = c.Client()
            plc.connect('10.10.10.101', 0, 1)
            data = plc.db_read(103, 0, 126)  # llegir db (numero_db,primer byte, longitud maxima)
            for o in range(0, 56, 4):
                values.append(get_real(data, o))
            for p in range(56, 102, 2):
                values.append(get_int(data, p))
            for q in range(102, 126, 2):
                alarmes.append(get_int(data, q))

            # values.append(self.set_lm(values[34]))
            state_lines = self.set_lm(values[34])
            for s in state_lines:
                values.append(s)
            values.append(values[12]-values[13])       #pc 103-104
            values.append(-values[14]-values[11])         #pc 102-109
            self.values = values
            self.alarmes = alarmes
            return True
        except:
            print('Error llegir dades S7')
            return False

    def set_lm(self,v):
        linies = format(v, "b")
        if len(linies) < 12:
            space = 12 - (len(linies))
            for i in range(space):
                linies = "0" + linies
        return [1, 1, 1, 1]

    def set_pc(self, v1, v2):
        return self.values[v1]-self.values[v2]

    def create_query(self, table, var):

        n = 'timestamp'
        s = '%s'
        for v in var:
            n = n+','+v
            s = s+',%s'

        sql = "INSERT INTO "+str(table)+" ("+n+") VALUES ("+s+")"
        return sql

    ''' Guardar al servidor moll'''

    def save_DB2(self,sql,data):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='otr',
                passwd='123456789',
                database='OTR')
            mycursor = mydb.cursor()
            mycursor.executemany(sql, [tuple(data)])
            mydb.commit()
            mydb.close()
            return True
        except:
            return False


    def decode_alarm(self):
        self.alarmCode = []
        alarm_binary = []
        #ajuntem totes les alarmes a una llista de valors hexadecimals
        for a in range(1,13):
            alarm_binary.append(format(self.alarmes[a], "016b"))
        alarm_bit = []
        for i in range(12):
            for j in range(15, -1, -1):
                alarm_bit.append(alarm_binary[i][j])
        alarm_pos = []
        # Comprovem que no hi hagin bits actius
        for k in range(192):
            if alarm_bit[k] == '1':
                alarm_pos.append(k+1)
        self.alarmCode = alarm_pos


    def readAlarms(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='otr',
                passwd='123456789',
                database='OTR')
            mycursor = mydb.cursor()
            sql = """SELECT * FROM alarmes """
            mycursor.execute(sql)
            var = mycursor.fetchall()
            # Alarmes de la DB en un JSON
            alarmesDB = {}
            for v in var:
                alarmesDB[v[1]] = v[2]
            mydb.close()
            # Compraracio de les alarmes escrites a la DB i les llegides per el bacnet
            for k in self.alarmCode:
                if k in alarmesDB:
                    del alarmesDB[k]
                else:
                    self.saveAlarm(str(k))
            for i in alarmesDB:
                self.deleteAlarm(i)
        except:
            pass

    def deleteAlarm(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='otr',
                passwd='123456789',
                database='OTR')
            mycursor = mydb.cursor()
            sql = "DELETE FROM alarmes WHERE alarmNumber='" + keyAlarma + "'"
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
            print('done Delete Alarmes mariaDB')
        except:
            print('error delete Alarmes ')

    def saveAlarm(self,keyAlarma):
        # try:
        print(type(keyAlarma))
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='otr',
            passwd='123456789',
            database='OTR')
        mycursor = mydb.cursor()
        sql = """INSERT INTO alarmes(timestamp,alarmNumber,missatge) VALUES(%s,%s,%s)"""
        print([tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyAlarma,self.alarmsJson[keyAlarma]])])
        mycursor.executemany(sql, [tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),keyAlarma,self.alarmsJson[keyAlarma]])])
        mydb.commit()
        mydb.close()
        print('done save Alarmes actives')
        # except:
        #     print('error save Alarmes ')

    def getKeys(self):
        file = open(self.file)
        dicConfig = json.load(file)
        file.close()
        return dicConfig

variables = ['Feedback_V101', 'Pot_cremador', 'Feedback_V002', 'TE101', 'TE105',
             'TE107', 'TE108', 'TE111', 'TE112', 'TE113', 'PT102', 'PT103', 'PT104', 'PT109',
             'Estat_OTR', 'V101', 'V102', 'V001', 'V011', 'V012', 'V013', 'V021', 'V022',
             'V023', 'V031', 'V032', 'V033', 'V401', 'V402', 'V403', 'V404', 'V405', 'V406',
             'V407', 'V408', 'Estat_linies', 'Estat_filtres', 'linia1', 'linia2','linia3',
             'linia4','PC_103_104', 'PC_102_109']


v = Values(variables)

while(True):
    try:
        v.read_variables()                          # Llegir les variables del PLC
        v.decode_alarm()                            # Decodificar alarmes binary to enter
        v.save_DB2(v.sql_data, v.get_values())      # Guardar les dades d'estat de la OTR a la base de dades
        v.readAlarms()                              # Llegir les variables de la DB-ot per actualitzar la llista amb les noves alarmes o borrar les que ja no estan actives
        time.sleep(10)
    except KeyboardInterrupt:
        raise
    except e as Exception:
        print('error: ',e)
        time.sleep(10)