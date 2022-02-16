import mysql.connector
import time
import telebot
import numpy as np
import openpyxl
import sys
import threading

from datetime import datetime
from datetime import timedelta

chat_id = ['743717839', '815134963', '1259688712', '409835547', '1772890260','2103459791','2103459926','857156986']



class Alarm_aspiracio:
    def __init__(self):
        self.a = [0, 0, 0, 0, 0]    #Alarma acutal
        self.la = [0, 0, 0, 0, 0]   #Alarma anterior
        self.lt = datetime(1994, 1, 14, 14, 30)
        self.t = datetime.now()
        self.messages = {}

        self.read_excel()

    def get_a(self):
        return self.a

    def get_la(self):
        return self.la

    def get_time(self):
        return self.t

    def get_ltime(self):
        return self.lt

    def set_a(self, a):
        self.a = a

    def set_la(self, a):
        self.la = a

    def set_ltime(self, t):
        self.lt = t

    def set_time(self, t):
        self.t = t

    def read_excel(self):
        book = openpyxl.load_workbook('/home/user/Telegram/Alarmes_telegram_socket.xlsx')
        sheet = book.active
        self.messages = {}
        for i in range(2, 233):
            c1 = "B" + str(i)
            c2 = "C" + str(i)
            self.messages[sheet[c1].value] = sheet[c2].value

    def get_message(self,n):
        return self.messages[n]


class Consum:

    def __init__(self):
        self.c = 0
        self.t = datetime.now()
        self.c_a = 0
        self.state = 0

    def get_c(self):
        return self.c, self.state, self.t

    def set_c(self, c):
        self.c_a = self.c
        self.c = c
        self.t = datetime.now()
        self.state_line()

    def state_line(self):
        # 0 estat parat, 1 engegant, 2 marxa ,3 parant
        self.state_a = self.state
        if self.c <= 5 and self.c_a <= 5:
            self.state = 0
        elif self.c > 5 >= self.c_a:
            self.state = 1
        elif self.c > 5 and self.c_a > 5:
            self.state = 2
        elif self.c < 5 < self.c_a:
            self.state = 3

    def __str__(self):
        return "Consum: "+str(self.c)+"  Estat: "+str(self.state)

class state_otr:
    def __init__(self):
        self.s = 6
        self.s_a = 6
        self.timestamp = datetime.now()

    def get_s(self):
        return self.s, self.s_a, self.timestamp

    def set_s(self, s, timestamp):
        self.s_a = self.s
        self.timestamp = timestamp
        self.s = s

    def __str__(self):
        return str(self.s)+' '+str(self.s_a)

class stateWS:
    def __init__(self):
        self.s = 0
        self.s_a = 0
        self.timestamp = datetime.now()

    def get_s(self):
        return self.s, self.s_a, self.timestamp

    def set_s(self, s, timestamp):
        self.s_a = self.s
        self.timestamp = timestamp
        self.s = s

    def __str__(self):
        return str(self.s)+' '+str(self.s_a)

class compressors:
    def __init__(self):
        self.p = 6.5
        self.p_a = 6.5
        self.s125 = 3
        self.s125_a = 3
        self.s125v = 3
        self.s125v_a = 3
        self.s100 = 0
        self.s100_a = 0
        self.timestampP = datetime.now()
        self.timestampS = datetime.now()

    def get_p(self):
        return self.p, self.p_a, self.timestampP

    def set_p(self,p,timestamp):
        self.p_a = self.p
        self.timestampP = timestamp
        self.p = p

    def get_s(self):
        return self.s125, self.s125_a, self.s125v, self.s125v_a, self.s100, self.s100_a, self.timestampS

    def set_s(self,s125, s125v, s100, timestamp):
        self.s125_a = self.s125
        self.s125v_a = self.s125v
        self.s100_a = self.s100

        self.timestampS = timestamp
        self.s125 = s125
        self.s125v = s125v
        self.s100 = s100

    def __str__(self):
        return str(self.p)+' '+str(self.p_a)


class Telegram:

    def __init__(self):

        self.t0 = datetime.now()-timedelta(minutes=1)
        self.bitComp = 0
        self.lastAlarmOTR = []
        self.lastAlarm = []
        self.readLastAlarmBio()




    def readAlarmesBio(self):
        mydb = mysql.connector.connect(
            host= '192.100.101.40',
            user= 'biomassa',
            passwd= '123456789',
            database= 'biomassa')
        mycursor = mydb.cursor()
        sql = """SELECT * FROM alarmes """
        mycursor.execute(sql)
        var = mycursor.fetchall()
        mydb.close()
        values = {}
        for i in var:
            values[i[1]] = i[2]
        return values

    def readLastAlarmBio(self):
        self.lastAlarm = self.readAlarmesBio()
        print(self.lastAlarm.pop("TCTR_102_AL_NIVMAX_TREFRIGERACIO"))


    def sendAlarmBio(self):
        self.actualAlarm = {}
        self.actualAlarm = self.readAlarmesBio()
        for k in self.actualAlarm:
            print(k)
        for a in self.actualAlarm:
            if a in self.lastAlarm:
                pass
            else:
                mes = "🌲 *Biomassa*: \n"
                mes += self.actualAlarm[a]+' \n'
                print(mes)
        self.lastAlarm = self.actualAlarm

    def readAlarmesOTR(self):
        mydb = mysql.connector.connect(
            host= '192.100.101.40',
            user= 'otr',
            passwd= '123456789',
            database= 'OTR')
        mycursor = mydb.cursor()
        sql = """SELECT * FROM alarmes """
        mycursor.execute(sql)
        var = mycursor.fetchall()
        mydb.close()
        values = {}
        for i in var:
            values[i[1]] = i[2]
        return values


"""https://api.telegram.org/bot867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs/getUpdates"""
token = '867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs'

t = Telegram()

flag_reboot = 0
while(True):
    t.sendAlarmBio()
    time.sleep(1)
    #t.sendAlarmOTR()
