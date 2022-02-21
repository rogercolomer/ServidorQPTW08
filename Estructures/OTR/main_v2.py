import snap7.client as c

import serial
import time
import mysql.connector

from snap7.util import *
from snap7.snap7types import *
from sqliteIOT import SQLiteIOT
from datetime import datetime


class Values:
    def __init__(self, v, a):

        self.values = []
        self.alarmes = []
        self.alarm_code =[]
        v_arr = []
        a_arr = []
        for var in v:
            v_arr.append(var[0])
        for al in a:
            a_arr.append(al[0])
        self.sql_values = self.create_query('value', v_arr)
        self.sql_alarmes = self.create_query('alarmes', a_arr)

    def get_values(self):
        return self.values

    def get_alarmes(self):
        return self.alarmes

    def read_variables(self):
        # try:
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
        values.append(self.set_lm(values[34]))
        values.append(values[12]-values[13])       #pc 103-104
        values.append(-values[14]-values[11])         #pc 102-109
        self.values = values
        self.alarmes = alarmes
        #     return True
        # except:
        #     print('Error llegir dades S7')
        #     return False

    def set_lm(self,v):
        linies = format(v, "b")
        if len(linies) < 12:
            space = 12 - (len(linies))
            for i in range(space):
                linies = "0" + linies
        l1 = linies[1]
        l2 = linies[4]
        l3 = linies[7]
        l4 = linies[10]
        lm = int(l1 + l2 + l3 + l4, 2)
        lm= 15
        return lm

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

    def save_DB(self,sql,data):
        # try:
        mydb = mysql.connector.connect(
            host='192.100.101.25',
            user='otr',
            passwd='123456789',
            database='OTR')
        mycursor = mydb.cursor()
        mycursor.executemany(sql, [tuple(data)])
        mydb.commit()
        mydb.close()
        return True
        # except:
        #     return False
    def decode_alarm(self):

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
                alarm_pos.append(k)
        # Omplim la matriu d'alarmes decodificades len = 5
        if len(alarm_pos)<5:
            while len(alarm_pos) < 5:
                alarm_pos.append(0)
        else:
            alarm_pos = [alarm_pos[0], alarm_pos[1], alarm_pos[2], alarm_pos[3], alarm_pos[4]]
        for i in range(5):
            self.alarmes.append(alarm_pos[i])


variables = [['Feedback_V101', 2, 1], ['Pot_cremador', 2, 1], ['Feedback_V002', 2, 1], ['TE101', 2, 1], ['TE105', 2, 1],
             ['TE107', 2, 1], ['TE108', 2, 1], ['TE111', 2, 1], ['TE112', 2, 1], ['TE113', 2, 1], ['PT102', 2, 1],
             ['PT103', 2, 1], ['PT104', 2, 1], ['PT109', 2, 1], ['Estat_OTR', 2, 1], ['V101', 2, 1], ['V102', 2, 1],
             ['V001', 2, 1], ['V011', 2, 1], ['V012', 2, 1], ['V013', 2, 1], ['V021', 2, 1], ['V022', 2, 1],
             ['V023', 2, 1], ['V031', 2, 1], ['V032', 2, 1], ['V033', 2, 1], ['V401', 2, 1],['V402', 2, 1],
             ['V403', 2, 1], ['V404', 2, 1], ['V405', 2, 1], ['V406', 2, 1], ['V407', 2, 1],['V408', 2, 1],
             ['Estat_linies', 2, 1], ['Estat_filtres', 2, 1], ['lm', 2, 1], ['PC_103_104', 2, 1], ['PC_102_109', 2, 1]]

alarmes = [['ATipo1', 2, 1], ['ATipo2', 2, 1], ['ATipo3', 2, 1], ['ATipo4', 2, 1], ['ATipo5', 2, 1],
           ['ATipo6',  2, 1], ['ATipo7', 2, 1], ['ATipo8', 2, 1], ['ATipo9', 2, 1], ['ATipo10', 2, 1],
           ['ATipo11', 2, 1], ['ATipo12', 2, 1], ['alarma0', 2, 1], ['alarma1', 2, 1], ['alarma2', 2, 1],
           ['alarma3', 2, 1], ['alarma4', 2, 1]]

l_val = SQLiteIOT('machine.db', 'PLANA', variables)
l_al = SQLiteIOT('machine.db', 'alarms', alarmes)
while(True):
    v = Values(variables, alarmes)
    v.read_variables()

    # lite.insert_machine(u.get_A())
    print(tuple(v.values))
    print(tuple(v.alarmes))
    v.decode_alarm()
    v.save_DB(v.sql_values, v.get_values())
    v.save_DB(v.sql_alarmes, v.get_alarmes())
    time.sleep(3)
