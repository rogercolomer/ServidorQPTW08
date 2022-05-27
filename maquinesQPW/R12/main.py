# from sqliteIOT import
# *
from machineIOT import ModbusRTU
from datetime import datetime, timedelta
import time
import logging
import mysql.connector
import json
import sys


class Fisico:
    def __init__(self):

        self.varCom = self.readConfig()

        self.FechaHoraInici = datetime.now().replace(microsecond=0)
        self.FechaHora = self.FechaHoraInici + timedelta(seconds=60)    # hora final
        self.FechaHoraActual = None                                     #para enviar la ntoficacion y averias en fase
        self.EstadoLinea = 0
        self.Buenas = 0
        self.Procesadas = 0

        self.alarmes = []

        self.registre = None
        self.registreBones = 0
        self.registreProce = 0
        self.registreEstat = 0
        self.registreBonesLast = 0
        self.registreProceLast = 0
        self.alarmArray = []
        self.bitParada = 0
        self.bitCanviTorn = 0
        self.limitRegistre = 4294967295

        self.FechaHoraActual = None

        self.alarmaActiva = 0
        self.MarchaMaquina = 0
        self.fechaParadaIncio = None
        # aquest valor ens dona informacio de quin protocol s'utilizara quines variables treballar
        # i a com s'hi connectara

        self.initComunicacio()

        self.badRead = 0     # variable errorReadData
        self.bitNotiError = 0


    def upgradeDate(self):
        self.FechaHoraInici = datetime.now().replace(microsecond=0)
        self.FechaHora = self.FechaHoraInici + timedelta(seconds=60)  # hora final

    def readConfig(self):
        file = open("/home/root/config.json")
        dicConfig = json.load(file)
        file.close()
        return dicConfig

    def resetValues(self):
        self.Procesadas = 0
        self.Buenas = 0
        self.alarmes = []

    def initComunicacio(self):
        '''la variable registre es defineix com la classe comunicació on si guarden totes les
        dades de la comunicacio'''
        if self.varCom['protocol'] == 'ModbusTCP':
            self.registre = Modbus(self.varCom['variables'], self.varCom['ip'])
            if self.lecturaDada():
                if self.registreEstat == 1:
                    self.EstadoLinea = 1
                    self.saveFisico()
                else:
                    self.EstadoLinea = 2
                    self.bitParada = 1
                    self.saveFisico()

        elif self.varCom['protocol'] == "RS232 2050":
            self.registre = UART(self.varCom['variables'], port='/dev/ttyUSB0')
            self.lecturaDada()
            if self.lecturaDada():
                if self.registreEstat == 1:
                    self.EstadoLinea = 1
                    self.saveFisico()
                else:
                    self.EstadoLinea = 2
                    self.bitParada = 1
                    self.saveFisico()
        elif self.varCom['protocol'] == "USB":
            self.registre = USB(self.varCom['variables'])
            self.lecturaDada()
            if self.lecturaDada():
                if self.registreEstat == 1:
                    self.EstadoLinea = 1
                    self.saveFisico()
                else:
                    self.EstadoLinea = 2
                    self.bitParada = 1
                    self.saveFisico()
        elif self.varCom['protocol'] == 'ModbusRTU':
            self.registre = ModbusRTU(self.varCom['variables'], port='/dev/ttyS2')
            if self.lecturaDada():
                if self.registreEstat == 1:
                    self.EstadoLinea = 1
                    self.saveFisico()
                else:
                    self.EstadoLinea = 2
                    self.bitParada = 1
                    self.saveFisico()
        elif self.varCom['protocol'] == 'Snap7':
            self.registre = S7(self.varCom['variables'], host=self.varCom['ip'], db=self.varCom['db'])
            if self.lecturaDada():
                if self.registreEstat == 1:
                    self.EstadoLinea = 1
                    self.saveFisico()
                else:
                    self.EstadoLinea = 2
                    self.bitParada = 1
                    self.saveFisico()

    def lecturaDada(self):
        try:
            sMach = self.registre.readData()
        except:
            sMach = False
            print('Error lectura dada')

        # TODO falta condicio de si no hi ha data
        if sMach == 1:
            self.registreProce = self.registre.dataA[0]
            self.registreBones = self.registre.dataA[1]
            # estat de mauqina
            if self.registre.dataA[2] == 0:
                self.registreEstat = 2
            else:
                self.registreEstat = self.registre.dataA[2]
            return True
        else:
            return False

    def mainData(self):
        self.registreProceLast = self.registreProce
        self.registreBonesLast = self.registreBones
        self.registreEstatLast = self.registreEstat
        if self.lecturaDada():
            procesadas = self.registreProce - self.registreProceLast
            buenas = self.registreBones - self.registreBonesLast
            # print(buenas,procesadas,self.registreEstat)
            try:
                if procesadas < 0:
                    procesadas = (self.registreProce + self.limitRegistre) - self.registreProceLast
                if procesadas > 100:
                    procesadas = 0
                if buenas < 0:
                    buenas = (self.registreBones + self.limitRegistre) - self.registreBonesLast
                if buenas > 100:
                    buenas = 0
                if self.varCom['variables'][1][2] == 0:
                    buenas = procesadas
                self.Procesadas += procesadas
                self.Buenas += buenas

                if datetime.now().hour == 6 and datetime.now().minute == 0 and datetime.now().second == 0 and self.bitCanviTorn == 0 or \
                    datetime.now().hour == 14 and datetime.now().minute == 0 and datetime.now().second == 0 and self.bitCanviTorn == 0 or \
                    datetime.now().hour == 22 and datetime.now().minute == 0 and datetime.now().second == 0 and self.bitCanviTorn == 0:
                    self.saveFisico()
                    self.bitCanviTorn = 1
                elif self.bitCanviTorn == 1:
                    self.bitCanviTorn = 0
                else:
                    if self.registreEstat != self.registreEstatLast:
                        if self.registreEstat == 1:
                            self.EstadoLinea = 1
                            self.resetValues()
                        else:
                            self.EstadoLinea = 2
                        print(self.registreEstat, self.registreEstatLast, "Canvi estat")
                        self.saveFisico()
                        if self.EstadoLinea == 1:
                            if self.alarmaActiva == 1:
                                self.saveMotivosParada()
                                self.alarmaActiva = 0
                                print('Save alarma')
                        elif self.EstadoLinea == 2:
                            self.decodeAlarm()
                        self.resetValues()
                        self.bitParada = 1
                    if datetime.now() >= self.FechaHora:
                        self.upgradeDate()
                        if self.Buenas > 0 or self.Procesadas > 0:
                            if self.registreEstat == 1:
                                self.EstadoLinea = 1
                                self.saveFisico()
                                print(self.Procesadas, self.Buenas, self.EstadoLinea, self.MarchaMaquina, ' Funcionant')

                            elif self.registreEstat == 2:
                                self.EstadoLinea = 2
                                self.saveFisico()
                                self.decodeAlarm()
                                print(self.Procesadas, self.Buenas, self.EstadoLinea, self.MarchaMaquina, ' Sesta parant')
                            self.bitParada = 0
                        else:
                            if self.bitParada == 0:
                                self.EstadoLinea = self.registreEstat
                                self.saveFisico()
                                if self.EstadoLinea == 2:
                                    self.decodeAlarm()
                                print(self.Procesadas, self.Buenas, self.EstadoLinea, self.MarchaMaquina, ' Sha parat')
                                self.bitParada = 1
                        self.resetValues()

                    elif self.registreEstat == 2 and self.bitParada == 0:
                        self.bitParada = 1
                        self.EstadoLinea = 2
                        self.saveFisico()
                        self.decodeAlarm()
                        print(self.Procesadas, self.Buenas, self.EstadoLinea, ' Sha parat extra')
                        self.Procesadas = 0
                        self.Buenas = 0
            except:
                print('Error main Data')


    def saveFisico(self):
        try:
            self.FechaHoraActual = datetime.now()
            mydb = mysql.connector.connect(
                host='localhost',
                user='mesbook',
                passwd='123456789',
                database=self.varCom['linea'])
            mycursor = mydb.cursor()
            print(datetime.now(), self.EstadoLinea, self.varCom['nLinea'], self.Procesadas, self.Buenas)
            sql = """INSERT INTO fisico (FechaHora, Estadolinea, Linea, Procesadas, Buenas) VALUES
                     (%s,%s,%s,%s,%s)"""
            mycursor.executemany(sql, [tuple([self.FechaHoraActual, self.EstadoLinea, self.varCom['nLinea'], self.Procesadas,self.Buenas])])
            mydb.commit()
            mycursor.close()
            mydb.close()
        except:
            print('Error save Fisico')

    def decodeAlarm(self):
        try:
            self.fechaParadaIncio = self.FechaHoraActual
            self.alarmes = self.registre.dataA[3:]
            bin_alarm = []
            print(self.alarmes)
            for a in self.alarmes:
                bin_alarm.append(bin(a)[2:].zfill(16))
            comptador_al = 0
            al_num = []
            for k in bin_alarm:
                for j in range(15, -1, -1):
                    if k[j] == '1':
                        if comptador_al+1 == 200 :
                            pass
                        else:
                            al_num.append(comptador_al+1)
                    comptador_al += 1
            if al_num:
                self.MarchaMaquina = al_num[0]
                self.alarmaActiva = 1
        except:
            print('Error decodeAlarm')

    def saveMotivosParada(self):
        try:
            mydb = mysql.connector.connect(
                host='localhost',
                user='mesbook',
                passwd='123456789',
                database=self.varCom['linea'])
            mycursor = mydb.cursor()
            # print(datetime.now(), self.EstadoLinea, self.varCom['nLinea'], self.Procesadas,self.Buenas)
            sql = """INSERT INTO motivosParada (fechaHoraInicio, fechaHoraFin, Linea, MarchaMAquina) VALUES
                     (%s,%s,%s,%s)"""
            mycursor.executemany(sql, [tuple([self.fechaParadaIncio, self.FechaHoraActual, self.varCom['nLinea'], self.MarchaMaquina])])
            print([self.fechaParadaIncio, self.FechaHoraActual, self.varCom['nLinea'], self.MarchaMaquina])
            mydb.commit()
            mycursor.close()
            mydb.close()
        except:
            print('Error save motivos parada')

    def errorReadData(self, state):
        '''
        :param state: boolean good or bad read
        :return: empty
        '''
        if state == True:
            self.badRead = 0
            if self.bitNotiError == 1:
                self.saveError(0)
            self.bitNotiError = 0
        else:
            self.badRead += 1
            print('error', self.badRead)

        if self.badRead >= 100 and self.bitNotiError == 0:
            print('guardar a la base de dades')
            self.saveError(1)
            self.bitNotiError = 1
        return state

    def saveError(self, estat):
        '''
        :param estat:
        :return:
        '''
        try:
            mydb = mysql.connector.connect(
                host='localhost',
                user='mesbook',
                passwd='123456789',
                database=self.varCom['linea'])
            mycursor = mydb.cursor()
            # print(datetime.now(), self.EstadoLinea, self.varCom['nLinea'], self.Procesadas,self.Buenas)
            sql = """INSERT INTO errors (fechaHora, error) VALUES
                     (%s,%s)"""
            mycursor.executemany(sql, [tuple([datetime.now(), estat])])
            mydb.commit()
            mycursor.close()
            mydb.close()
        except:
            print('Error save motivos parada')


f = Fisico()

while True:
    try:
        f.mainData()
        time.sleep(0.5)
    except KeyboardInterrupt:
        raise
    except:
        print('error general')
        time.sleep(2)


