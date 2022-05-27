import mysql.connector
import time
import telebot
import numpy as np
import openpyxl
import sys
import threading
import json
from datetime import datetime, timedelta

# chat_id = ['743717839', '815134963', '1259688712', '409835547', '1772890260','2103459791','2103459926','857156986']
# time.sleep(60)

# "815134963":  {"usuari": "Josep Faja"},
#   "1259688712": {"usuari": "Isaac Espaulella" },
#   "409835547":  {"usuari": "Joan Colomer"},
#   "1772890260": {"usuari": "Arnau Arboix"},
#   "2103459791": {"usuari": "Raul Gomez"},
#   "2103459926": {"usuari": "Nil Muntala"},
#   "857156986":  {"usuari": "Ibrahim Amar"}

def getKeys():
    file = open("/home/roger/repositori/ServidorQPWood/Telegram/usersAlarmesTM.json")
    dicConfig = json.load(file)
    file.close()
    return dicConfig

chat_id = getKeys()


class Consum:

    def __init__(self):
        self.c = 10
        self.t = datetime.now()
        self.c_a = 10
        self.state = 2

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
        self.ln = ['L01', 'L02', 'L03', 'L04', 'L05', 'L06', 'L07','L08', 'L11', 'L13']
        self.co = {}
        self.init_consums()
        self.s_OTR = state_otr()
        self.t0 = datetime.now()-timedelta(minutes=1)
        self.dicWS ={}
        self.dicWS['state'] = stateWS()
        self.dicWS['qptw04'] = stateWS()
        self.comp = compressors()
        self.bitComp = 0
        self.lastAlarmOTR = []
        self.lastAlarm = []
        self.lastAlarmAspriacio = []
        self.readLastAlarmBio()
        self.readLastAlarmOTR()
        self.readLastAlarmAspiracio()

        self.ndAspiracio = 0        # Done
        self.ndOTR = 0              # Done
        self.ndCompressorsS = 0
        self.ndCompressorsP = 0
        self.ndBiomassa = 0
        self.ndQPTW04 = 0           # Done
        self.ndQPTW05 = 0           #Done
        self.ndConsumsQ = 0



    def init_consums(self):
        try:
            for l in self.ln:
                self.co[l] = Consum()
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='telegram',
                passwd='123456789',
                database='aspiracio')

            sql = "SELECT * FROM consums ORDER BY timestamp DESC LIMIT 1"

            mycursor = mydb.cursor()
            mycursor.execute(sql)
            consums = mycursor.fetchall()
            for c, l in zip(range(1, 11), self.ln):
                self.co[l].set_c(consums[0][c])
            mydb.close()
        except Exception as e:
            time.sleep(10)
            print(e)



    def read_consums(self):
        try:
            mydb = mysql.connector.connect(
                    host='192.100.101.40',
                    user='telegram',
                    passwd='123456789',
                    database='aspiracio')

            sql = "SELECT * FROM consums ORDER BY timestamp DESC LIMIT 1"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            consums = mycursor.fetchall()
            self.ndAspiracio = self.compData(consums[0][0],self.ndAspiracio,"aspiracio",5)
            for c,l in zip(range(1, 11), self.ln):
                self.co[l].set_c(consums[0][c])
            mydb.close()
            print(consums)
            return True
        except Exception as e:
            time.sleep(10)
            print(e)

    def send_paros(self):
        try:
            for l in self.ln:
                c, s, time = self.co[l].get_c()
                print(l, c, s)
                if s == 1 :
                    mes = "🏭 *ASPIRACIÓ:* La  " + l + " s'esta engegant"
                    self.send_mes(mes)
                elif s == 3:
                    mes = "🏭 *ASPIRACIÓ:* La  " + l + " ha deixat de funcionar"
                    self.send_mes(mes)
                else:
                    pass
        except:
            print('error Paros')

    def read_state_OTR(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='telegram',
                passwd='123456789',
                database='OTR')

            sql = "SELECT timestamp,Estat_OTR FROM data ORDER BY timestamp DESC LIMIT 1"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            state = mycursor.fetchall()
            self.ndOTR = self.compData(state[0][0], self.ndOTR, "OTR",5)
            mydb.close()
            self.s_OTR.set_s(int(state[0][1]), state[0][0])
            return True
        except Exception as e:
            time.sleep(10)

    def send_state_OTR(self):
        try:
            s, s_a, timestamp = self.s_OTR.get_s()
            if s == s_a :
                pass
            elif s == 1:
                mes = "*🔥 OTR:* La màquina està en estat de seguretat "
                self.send_mes(mes)
            elif s == 2:
                mes = "*🔥 OTR:* La màquina està en estat de repos "
                self.send_mes(mes)
            elif s == 3:
                mes = "*🔥 OTR:* La màquina està en estat de purga "
                self.send_mes(mes)
            elif s == 4:
                mes = "*🔥 OTR:* La màquina està en estat d'escalfament "
                self.send_mes(mes)
            elif s == 5:
                mes = "*🔥 OTR:* La màquina està en estat de commutació "
                self.send_mes(mes)
            elif s == 6:
                mes = "*🔥 OTR:* La màquina està correcte"
                self.send_mes(mes)
            elif s == 7:
                mes = "*🔥 OTR:* La màquina està en estat de parada "
                self.send_mes(mes)
            elif s == 8:
                mes = "*🔥 OTR:* La màquina està en estat de refredament "
                self.send_mes(mes)
            elif s == 9:
                mes = "*🔥 OTR:* La màquina està en estat de parada de variadors "
                self.send_mes(mes)
            elif s == 10:
                mes = "*🔥 OTR:* La màquina està en estat de standby "
                self.send_mes(mes)
            else:
                pass
        except:
            print('error OTR')

    def readStateWS(self,table):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='roger',
                passwd='123456789',
                database='monitorWS')

            sql = "SELECT FechaHora, state FROM "+table+" ORDER BY FechaHora DESC LIMIT 1"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            state = mycursor.fetchall()

            mydb.close()
            self.dicWS[table].set_s(int(state[0][1]), state[0][0])
            self.sendStateWS(table)

        except Exception as e:
            print(e)
            time.sleep(10)

    def sendStateWS(self,table):
        s, s_a, timestamp = self.dicWS[table].get_s()

        if table == 'state':
            table = 'qptw05'
            self.ndQPTW05 = self.compData(timestamp, self.ndQPTW05, "QPTW05",5)
        if s == s_a:
            self.ndQPTW04 = self.compData(timestamp, self.ndQPTW04, "QPTW04",5)
        elif s == 1 and s_a == 0:
            self.send_mes_roger("*MesBook:*El WS "+table+" s'esta posant en marxa")
        elif s == 0 and s_a == 1:
            self.send_mes_roger("*MesBook:*El WS "+table+" sha parat")


    def readPresComp(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='roger',
                passwd='123456789',
                database='compressors')

            sql = "SELECT timestamp, pres FROM comp_sen ORDER BY timestamp DESC LIMIT 1"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            values = mycursor.fetchall()
            mydb.close()
            self.comp.set_p(float(values[0][1]), values[0][0])
            return True
        except Exception as e:
            print(e)
            time.sleep(10)

    def sendPresComp(self):
        try:
            p, p_a, timestamp = self.comp.get_p()
            if p < 6.3 and p_a < 6.3 and self.bitComp == 0:
                self.send_mes("*🏭 Compressors:*La pressió està per sota 6.3 Bars")
                self.bitComp = 1
            elif p > 6.3 and p_a < 6.3:
                self.send_mes("*🏭 Compressors:*La pressió ha tornat a pujar")
                self.bitComp = 0
            else:
                pass
        except:
            print('error SendPresComp')

    def readStateComp(self):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='roger',
                passwd='123456789',
                database='compressors')

            sql = "SELECT timestamp, r125, r125v, r100 FROM estat ORDER BY timestamp DESC LIMIT 1"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            values = mycursor.fetchall()
            mydb.close()
            self.comp.set_s(int(values[0][1]),int(values[0][2]), int(values[0][3]),  values[0][0])
            return True
        except Exception as e:
            print(e)
            time.sleep(10)

    def sendStateComp(self):

        s125, s125_a, s125v, s125v_a, s100, s100_a, timestamp = self.comp.get_s()
        if s125 == s125_a:
            mes125 = 0
        elif s125 == 0:
            mes125 = "*🏭 Compressor*: R125 aturat manual "
        elif s125 == 1:
            mes125 = "*🏭 Compressor*: R125 marxa manual "
        elif s125 == 2:
            mes125 = "*🏭 Compressor*: R125 aturat en automàtic "
        elif s125 == 3:
            mes125 = "*🏭 Compressor*: R125 marxa automàtic "

        if s125v == s125v_a:
            mes125v = 0
        elif s125v == 0:
            mes125v = "*🏭 Compressor*: R125V aturat manual "
        elif s125v == 1:
            mes125v = "*🏭 Compressor*: R125V marxa manual "
        elif s125v == 2:
            mes125v = "*🏭 Compressor*: 125V aturat en automàtic "
        elif s125v == 3:
            mes125v = "*🏭 Compressor*: 125V marxa automàtic "

        if s100 == s100_a:
            mes100 = 0
        elif s100 == 0:
            mes100 = "*🏭 Compressor*: R100 aturat manual "
        elif s100 == 1:
            mes100 = "*🏭 Compressor*: R100 marxa manual "
        elif s100 == 2:
            mes100 = "*🏭 Compressor*: R100 aturat en automàtic "
        elif s100v == 3:
            mes100 = "*🏭 Compressor*: R100 marxa automàtic "

        if mes125 != 0:
            self.send_mes(mes125)
        if mes125v != 0:
            self.send_mes(mes125v)
        if mes100 != 0:
            self.send_mes(mes100)

    def readAlarmesBio(self):
        try:
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
        except:
            print('error read Alarmes Bio')
            return None

    def readLastAlarmBio(self):
        self.lastAlarm = self.readAlarmesBio()

    def sendAlarmBio(self):
        try:
            self.actualAlarm = {}
            self.actualAlarm = self.readAlarmesBio()
            for a in self.actualAlarm:
                if a in self.lastAlarm:
                    pass
                else:
                    mes = "🌲 *Biomassa*: \n"
                    mes += self.actualAlarm[a]+' \n'
                    self.send_mes_colomer(mes)
            self.lastAlarm = self.actualAlarm
            print(self.actualAlarm)
        except:
            print('error send Alarm Bio')

    def readAlarmesOTR(self):
        try:
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
        except:
            print('error readAlarmesOTR')
            return None


    def readLastAlarmOTR(self):
        self.lastAlarmOTR = self.readAlarmesOTR()

    def sendAlarmOTR(self):
        try:
            self.actualAlarmOTR = {}
            self.actualAlarmOTR = self.readAlarmesOTR()
            for a in self.actualAlarmOTR:
                if a in self.lastAlarmOTR:
                    pass
                else:
                    mes = "🔥 *OTR*: \n"
                    mes += self.actualAlarmOTR[a]+' \n'
                    self.send_mes_colomer(mes)
            self.lastAlarmOTR = self.actualAlarmOTR
        except:
            print('error sendAlarmOTR')

    #Aspiracio
    def readAlarmesAspiracio(self):
        try:
            mydb = mysql.connector.connect(
                host= '192.100.101.40',
                user= 'aspiracio',
                passwd= '123456789',
                database= 'aspiracio')
            mycursor = mydb.cursor()
            sql = """SELECT * FROM alarma """
            mycursor.execute(sql)
            var = mycursor.fetchall()
            mydb.close()
            values = {}
            for i in var:
                values[i[2]] = i[1]
            return values
        except:
            print('error readAlarmesAspiracio')
            return None

    def readLastAlarmAspiracio(self):
        self.lastAlarmAspiracio = self.readAlarmesAspiracio()

    def sendAlarmAspiracio(self):
        try:
            self.actualAlarmAspiracio = {}
            self.actualAlarmAspiracio = self.readAlarmesAspiracio()
            for a in self.actualAlarmAspiracio:
                if a in self.lastAlarmAspiracio:
                    pass
                else:
                    mes = "🏭 *Aspiracio*: \n"
                    mes += self.actualAlarmAspiracio[a]+' \n'
                    self.send_mes(mes)
            self.lastAlarmAspiracio = self.actualAlarmAspiracio
        except:
            print('error sendAlarmAspriacio')

    def send_mes_roger(self,m):
        try:
            c = '743717839'
            tb.send_message(c, text=str(m), parse_mode="Markdown")
            print(c+' :'+str(m))
        except Exception as e:
            time.sleep(10)
            print('erro send message')

    def send_mes_colomer(self,m):
        try:
            c = '743717839'
            tb.send_message(c, text=str(m), parse_mode="Markdown")
            c = '409835547'
            tb.send_message(c, text=str(m), parse_mode="Markdown")
            print(c+' :'+str(m))
        except Exception as e:
            time.sleep(10)
            print('erro send message')

    def send_mes(self,m):
        for c in chat_id:
            try:
                tb.send_message(c, text=str(m), parse_mode="Markdown")
                print(c+' :'+str(m))
            except Exception as e:
                print(e)

    def imAlive(self):
        self.send_mes_roger('*Estat Telegram:* Estem vius 😄 ')

    def readNoValue(self,database,table):
        try:
            mydb = mysql.connector.connect(
                host='192.100.101.40',
                user='roger',
                passwd='123456789',
                database=database)

            sql = "SELECT * FROM "+table+" ORDER BY timestamp DESC LIMIT 1"
            mycursor = mydb.cursor()
            mycursor.execute(sql)
            values = mycursor.fetchall()
            if database == 'biomassa':
                self.ndBiomassa = self.compData(values[0][0], self.ndBiomassa, "Biomassa",5)
            elif database == "consums":
                self.ndConsumsQ = self.compData(values[0][0], self.ndConsumsQ, "Consums Quart-Horaris",20)
            mydb.close()

            return True
        except Exception as e:
            print(e)
            time.sleep(10)

    def compData(self,timestamp, bitPas, sistema, minND):
        if timestamp < datetime.now() - timedelta(minutes=minND) and bitPas == 0:
            self.send_mes_roger("*Estat Telegram:* L'"+sistema+" no te dades")
            bitPas = 1
        elif timestamp < datetime.now() - timedelta(minutes=1):
            pass
        else:
            bitPas = 0
        return bitPas


"""https://api.telegram.org/bot867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs/getUpdates"""
token = '867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs'

t = Telegram()

flag_reboot = 0
while(True):
    try:
        tb = telebot.TeleBot(token)
        r_c = t.read_consums()
        if r_c:
            t.send_paros()
        r_so = t.read_state_OTR()
        if r_so:
            t.send_state_OTR()
        t.readStateWS('state')
        t.readStateWS('qptw04')

        r_comp = t.readPresComp()
        if r_comp:
            t.sendPresComp()
        r_Scomp = t.readStateComp()
        if r_Scomp:
            t.sendStateComp()
        t.sendAlarmBio()
        t.sendAlarmOTR()
        t.sendAlarmAspiracio()
        if datetime.now().hour == 8:
            if flag_reboot == 0:
                t.imAlive()
                flag_reboot = 1
        elif datetime.now().hour == 1 and flag_reboot == 1:
            flag_reboot = 0
        t.readNoValue("biomassa", "estatTemp")
        t.readNoValue("consums", "tarifaQuarthoraria")
        tb.stop_bot()
        time.sleep(10)
    except KeyboardInterrupt:
        raise
    except Exception as e:
            time.sleep(10)
            print(e)
