import mysql.connector
import openpyxl

import sqlite3
import json
import snap7.client as c
from snap7.util import *
# from snap7.snap7types import *
from datetime import datetime
from time import sleep


def UintDuint(c0, c1):
    s0 = hex(c0)[2:len(hex(c0))]  # concatenem els dos parells de bytes en 4 bytes junts per fer una DUINT
    s1 = hex(c1)[2:len(hex(c1))]
    # omplim les string amb 0's peque es puguin concatenar (4 valors hex cada una )
    # quan es concatenin tindran 8 valors hex que són 32 bits
    while len(s0) < 4:
        s0 = '0' + s0
    while len(s1) < 4:
        s1 = '0' + s1
    t = (s1 + s0)
    return int(t, 16)


class Alarm:
    def __init__(self):
        self.a = 0

    def set_alarm(self, a):
        self.a = a

    def get_alarm(self):
        return self.a


class Consum:
    def __init__(self):
        self.c = 5

    def set_consum(self, c):
        self.c = c

    def get_consum(self):
        return self.c

    def __str__(self):
        val = "El consum de la línia " + str(self.c) + " A "
        return val


class Bucle:
    def __init__(self, alarmes):
        self.valors = {}
        self.alarms = {}
        self.alarm_code = []
        self.alarm_list = alarmes
        self.vibracions = []
        self.nivells = []
        self.counters = []
        self.file = '/home/root/alarmes.json'
        self.alarmsJson = self.getKeys()

    def add_alarm(self, n):
        self.alarms[n] = Alarm()

    def add_consum(self, n):
        self.valors[n] = Consum()

    def __str__ (self):
        s_v = ''
        for k in self.valors:
            s_v = s_v + 'El consum de la ' + k + ' es de ' + str(self.valors[k].get_consum()) + ' A \n'
        return s_v

    def get_alarms(self):
        print('get alarms')
        s_a = ''
        for k in self.alarms:
            s_a = s_a + "La alarma" + k + " te el valor " + str(self.alarms[k].get_alarm()) + '\n'
        print(s_a)
    def set_consums(self, c):
        for k, i in zip(sorted(self.valors), range(len(self.valors))):
            self.valors[k].set_consum(c[i])

    def set_alarmes(self, a):
        for k, i in zip(sorted(self.alarms), range(len(self.alarms))):
            self.alarms[k].set_alarm(a[i])

    def getKeys(self):
        file = open(self.file)
        dicConfig = json.load(file)
        file.close()
        return dicConfig

    def read_consums(self):
        val = []
        plc = c.Client()
        plc.connect('x.x.x.x', 0, 1)
        data0 = plc.db_read(100, 0, 32)     # llegir db (numero_db,primer byte, longitud maxima)
        for i in range(0, 32, 4):
            val.append(get_real(data0, i))
        data1 = plc.db_read(100, 40, 4)
        val.append(get_real(data1, 0))
        data2 = plc.db_read(100, 48, 2)     # llegir db (numero_db,primer byte, longitud maxima)
        val.append(int.from_bytes(data2, "big") / 10)
        plc.disconnect()
        self.set_consums(val)

    def read_alarms(self):
        plc = c.Client()
        plc.connect('x.x.x.x', 0, 1)
        data3 = plc.db_read(100, 50, 37)     # llegir db (numero_db,primer byte, longitud maxima)296 booleans
        list_alarm = []
        for i in data3:
            list_alarm.append(bin(i)[2:].zfill(8))
        self.set_alarmes(list_alarm)
        self.decode_alarm()
        plc.disconnect()

    def read_vib(self):
        plc = c.Client()
        plc.connect('x.x.x.x', 0, 1)
        data3 = plc.db_read(100, 88, 4)  # llegir db (numero_db,primer byte, longitud maxima)
        list_vib = []
        for i in range(0, 4, 2):
            list_vib.append(int.from_bytes([data3[i], data3[i+1]],byteorder='big', signed=False))
        self.vibracions = list_vib
        plc.disconnect()
        # self.set_alarmes(list_alarm)
        # self.decode_alarm()

    def read_nivells(self):
        plc = c.Client()
        plc.connect('x.x.x.x', 0, 1)
        data3 = plc.db_read(100, 92, 2)  # llegir db (numero_db,primer byte, longitud maxima)

        lebels = format(int.from_bytes([data3[0], data3[1]],byteorder='big', signed=False),'016b')

        self.nivells = []
        self.counters = []
        for i in range(15, 4, -1):
            self.nivells.append(lebels[i])
        plc.disconnect()
        plc = c.Client()
        plc.connect('x.x.x.x', 0, 1)
        data3 = plc.db_read(100, 94, 16)  # llegir db (numero_db,primer byte, longitud maxima)
        list_count = []
        for i in range(0, 16, 2):
            list_count.append(int.from_bytes([data3[i], data3[i+1]],byteorder='big', signed=False))
        for i in range(4):
            self.counters.append(int(round(UintDuint(list_count[(i*2)+1], list_count[i*2])/1000,0)))
        plc.disconnect()


    def decode_alarm(self):
        comptador_al = 0
        al_num = []
        for k in self.alarm_list:
            for j in range(7, -1, -1):
                if self.alarms[k].get_alarm()[j] == '1':
                    if 80 < comptador_al+1 < 93 or \
                            comptador_al+1 ==  34 or \
                            comptador_al+1 ==  35 or \
                            comptador_al+1 ==  36 or \
                            comptador_al+1 ==  37 or \
                            comptador_al+1 ==  38 or \
                            comptador_al+1 ==  41 or \
                            comptador_al+1 == 162 or \
                            comptador_al+1 == 201 or \
                            comptador_al+1 == 182:
                        pass
                    else:
                        al_num.append(comptador_al+1)
                comptador_al += 1

        self.alarm_code = al_num

        mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
        mycursor = mydb.cursor()
        sql = """SELECT * FROM alarma """
        mycursor.execute(sql)
        var = mycursor.fetchall()
        # Alarmes de la DB en un JSON
        alarmesDB = {}
        for v in var:
            alarmesDB[v[2]] = v[1]
        mydb.close()
        # Compraracio de les alarmes escrites a la DB i les llegides per el bacnet
        for k in self.alarm_code:
            if k in alarmesDB:
                del alarmesDB[k]
            else:
                self.saveAlarm(str(k))
        print(alarmesDB)
        for i in alarmesDB:
            self.deleteAlarm(i)

    def deleteAlarm(self,keyAlarma):
        # try:
        print(keyAlarma)
        mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
        mycursor = mydb.cursor()
        sql = "DELETE FROM alarma WHERE alarmValue='" + str(keyAlarma) + "'"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        print('done Delete Alarmes mariaDB')
        # except:
        #     print('error delete Alarmes ')

    def saveAlarm(self,keyAlarma):
        # try:
        mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
        mycursor = mydb.cursor()
        sql = """INSERT INTO alarma(timestamp,alarmValue,missatge) VALUES(%s,%s,%s)"""
        print([tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), keyAlarma, self.alarmsJson[keyAlarma]])])
        mycursor.executemany(sql, [
            tuple([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), keyAlarma, self.alarmsJson[keyAlarma]])])
        mydb.commit()
        mydb.close()
        print('done save Alarmes actives')
        # except:
        #     print("Problema guardar alarmes")

    def save_master(self):
        #guardar els valors a la base de dades del linux per fer telegram
        try:
            self.save_consums('x.x.x.x')
            self.save_vib('x.x.x.x')
            self.save_nivells('x.x.x.x')
            return True
        except:
            return False

    def save_consums(self,ip):
        name_sql = 'timestamp'
        s_sql = '%s'
        values_sql = [datetime.now()]
        for k in sorted(self.valors):
            name_sql = name_sql +',Consum_'+k
            s_sql = s_sql+',%s'
            values_sql.append(self.valors[k].get_consum())
        sql = """INSERT INTO consums("""+name_sql+""") VALUES ("""+s_sql+""")"""

        mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
        mycursor = mydb.cursor()
        mycursor.executemany(sql, [tuple(values_sql)])
        mydb.commit()
        mydb.close()

    def save_vib(self, ip):
        sql = """INSERT INTO impulsio(timestamp, vibracio_analogia, vibracio_percentatge) VALUES (%s,%s,%s)"""

       mydb = mysql.connector.connect(
            host='x.x.x.x',
            user='user',
            passwd='passwd',
            database='database')
        mycursor = mydb.cursor()
        mycursor.executemany(sql, [(datetime.now(), self.vibracions[0], self.vibracions[1])])
        mydb.commit()
        mydb.close()

    def save_nivells(self, ip):
        self.estatB = 0
        tempsInc = self.counters[2] / 10
        if 0 <= self.counters[3] < tempsInc:
            self.estatB = 9
        elif tempsInc <= self.counters[3] < tempsInc * 2:
            self.estatB = 8
        elif tempsInc * 2 <= self.counters[3] < tempsInc * 3:
            self.estatB = 7
        elif tempsInc * 3 <= self.counters[3] < tempsInc * 4:
            self.estatB = 6
        elif tempsInc * 4 <= self.counters[3] < tempsInc * 5:
            self.estatB = 5
        elif tempsInc * 5 <= self.counters[3] < tempsInc * 6:
            self.estatB = 4
        elif tempsInc * 6 <= self.counters[3] < tempsInc * 7:
            self.estatB = 3
        elif tempsInc * 7 <= self.counters[3] < tempsInc * 8:
            self.estatB = 2
        elif tempsInc * 8 <= self.counters[3] < tempsInc * 9:
            self.estatB = 1
        elif tempsInc * 9 <= self.counters[3] :
            self.estatB = 0

        self.estatS2 = 0
        tempsInc = self.counters[0] / 8
        if self.nivells[3] == 1:
            self.estatS2 = 0
        elif 0 <= self.counters[1] < tempsInc:
            self.estatS2 = 9
        elif tempsInc <= self.counters[1] < tempsInc * 2:
            self.estatS2 = 8
        elif tempsInc * 2 <= self.counters[1] < tempsInc * 3:
            self.estatS2 = 7
        elif tempsInc * 3 <= self.counters[1] < tempsInc * 4:
            self.estatS2 = 6
        elif tempsInc * 4 <= self.counters[1] < tempsInc * 5:
            self.estatS2 = 5
        elif tempsInc * 5 <= self.counters[1] < tempsInc * 6:
            self.estatS2 = 4
        elif tempsInc * 6 <= self.counters[1] < tempsInc * 7:
            self.estatS2 = 3
        elif tempsInc * 7 <= self.counters[1] < tempsInc * 8:
            self.estatS2 = 2
        elif tempsInc * 8 <= self.counters[1] :
            self.estatS2 = 1

        sql = """INSERT INTO sitja(timestamp, migS1, maxS1, container, migS2, treballS2, maxS2, treballSB, maxSB, motorNivell, selSitja,VBiomassa,tempsS2prog, tempsS2trans, tempsBprog, tempsBtrans, estatBiomassa, estatS2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        mydb = mysql.connector.connect(
            host=ip,
            user='aspiracio',
            passwd='123456789',
            database='aspiracio')
        mycursor = mydb.cursor()
        print('estat',self.estatB)
        mycursor.executemany(sql, [(datetime.now(), self.nivells[0], self.nivells[1], self.nivells[2], self.nivells[3],
                                    self.nivells[4], self.nivells[5], self.nivells[6], self.nivells[7], self.nivells[8],
                                    self.nivells[9], self.nivells[10], self.counters[0], self.counters[1],
                                    self.counters[2], self.counters[3], self.estatB, self.estatS2)])
        mydb.commit()
        mydb.close()
        # print('goooo')


linies = ['L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'L07', 'L08', 'L11', 'L13']

alarmes = []
for i in range(37):
    if i<10:
        alarmes.append("a0"+str(i))
    else:
        alarmes.append("a"+str(i))
print(alarmes)
asp = Bucle(alarmes)
for l in linies:
    asp.add_consum(l)
for a in alarmes:
    asp.add_alarm(a)

while (True):
    try:
        asp.read_consums()
        asp.read_alarms()
        asp.read_vib()
        asp.read_nivells()

        if asp.save_master():
            print('Data master!')
            sleep(20)
        else:
            pass
    except Exception as e:
        print(e)

