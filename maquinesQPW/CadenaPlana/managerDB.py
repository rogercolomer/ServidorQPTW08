
import mysql.connector
import json
import requests
from datetime import datetime, timedelta
import urllib
import time

class mesbookDB():
    def __init__(self, db, user, pwd, host):
        self.dataBase = db
        self.user = user
        self.pwd = pwd
        self.host = host
        self.lastSendFisico = self.readRegFisico()
        self.lastSendParada = self.readRegParada()
        self.keyFisico = ('NumeroRegistro', 'FechaHora', 'EstadoLinea', 'Linea', 'Procesadas', 'Buenas')
        self.keyParada = ('NumeroRegistro', 'FechaHoraInicio', 'FechaHoraFin', 'Linea', 'MarchaMaquina')
        self.llistaFisico = []
        self.llistaParada = []
        self.urlFisico = "http://147.45.45.4:8000/api/productividad"
        self.urlParada = "http://147.45.45.4:8000/api/parada"
        self.sendOkFisico = False
        self.sendOkParada = False

    def getFisico(self):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            sql = """SELECT NumeroRegistro, FechaHora, EstadoLinea, Linea, Procesadas, Buenas FROM fisico WHERE NumeroRegistro>"""+str(self.lastSendFisico)+""" ORDER BY FechaHora """ #
            mycursor.execute(sql)
            var = mycursor.fetchall()
            mydb.close()
            return var
        except:
            return None

    def orderFisico(self, data):
        """ Ordena els valors de la base de dades en un Json"""
        llistaTrames = []   #Trames creade amb json
        self.llistaFisico = []     #trames creades amb diccionries python
        if data:
            for d in data:
                count = 0
                variables = dict.fromkeys(self.keyFisico)
                for k in variables:
                    if count==1:
                        variables[k] = str(d[count])
                    else:
                        variables[k] = int(d[count])
                    count += 1
                variables['Tramo'] = 1
                llistaTrames.append(json.dumps(variables))
                self.llistaFisico.append(variables)
            return self.llistaFisico
        else:
            return False

    def readRegFisico(self):
        """Lectura del fitxer la última trama enviada a mesbook """
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            sql = """SELECT FechaHora, registro FROM lectura WHERE registro IS NOT NULL ORDER BY FechaHora DESC LIMIT 1"""
            mycursor.execute(sql)
            var = mycursor.fetchall()
            mydb.close()
        except:
            pass
        try:
            self.lastSendFisico = var[0][1]
        except:
            self.lastSendFisico = 0


    def saveRegFisico(self):
        """Actualitzacio de lultm registre enviat
            S'ha de fer a la Base de dades taula lectura variable registro"""
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            # print(datetime.now(), self.EstadoLinea, self.nLinea, self.Procesadas, self.Buenas)
            sql = """INSERT INTO lectura (FechaHora, registro) VALUES (%s,%s)"""
            mycursor.executemany(sql,[tuple([datetime.now(), self.lastSendFisico])])

            sql = """DELETE FROM lectura WHERE registro<'""" + str(self.lastSendFisico-10000) + "'"
            mycursor.execute(sql)
            mydb.commit()

            mydb.commit()
            mydb.close()
        except:
            pass

    def deletePastFisico(self):
        try:
            """Elimina tots els registres anteriors a les 24hors abans de la ultima enviada"""
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            sql = "DELETE FROM fisico WHERE NumeroRegistro < "+str(self.lastSendFisico-10000)
            mycursor.execute(sql)
            mydb.commit()
            mydb.close()
        except:
            pass

        '''
        Enliminar de la base de dades trames antigues 
        '''

    def postFisico(self):
        notSend = []

        for ll in self.llistaFisico:
            try:
                response = requests.post(self.urlFisico, json=ll)
                print(len(self.llistaFisico))
                if response.status_code == 200:
                    print(len(self.llistaFisico), ll)
                    self.lastSendFisico = ll['NumeroRegistro']
                    self.sendOkFisico = False
                else:
                    notSend.append(ll)
            except:
                pass
                notSend.append(ll)
                print('not post')
                # TODO intentar de reenviar les trames no transmeses

        if self.sendOkFisico == False:
            try:
                self.saveRegFisico()
                self.sendOkFisico = True
                if not notSend:
                    self.deletePastFisico()
            except:
                pass
    """PARADA"""

    def getParada(self):
        try:
            print('LAST SEMD PARADA: ' +str(self.lastSendParada))
            if self.lastSendParada == None:
                self.lastSendParada = 0
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            sql = """SELECT NumeroRegistro, FechaHoraInicio, FechaHoraFin, Linea, MarchaMaquina FROM motivosParada WHERE NumeroRegistro>"""+str(self.lastSendParada)+""" ORDER BY FechaHoraInicio """ #
            mycursor.execute(sql)
            var = mycursor.fetchall()
            mydb.close()
            print(var)
            return var
        except:
            pass

    def orderParada(self, data):
        """ Ordena els valors de la base de dades en un Json"""
        if data:
            llistaTrames = []   #Trames creade amb json
            self.llistaParada = []     #trames creades amb diccionries python
            for d in data:
                count = 0
                variables = dict.fromkeys(self.keyParada)
                for k in variables:
                    if count==1 or count==2:
                        variables[k] = str(d[count])
                    else:
                        variables[k] = int(d[count])
                    count += 1
                # variables['Tramo'] = 1
                llistaTrames.append(json.dumps(variables))
                self.llistaParada.append(variables)
            return self.llistaParada
        else:
            return False

    def readRegParada(self):
        """Lectura del fitxer la última trama enviada a mesbook """
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            sql = """SELECT FechaHora, registroParadas FROM lectura WHERE registroParadas IS NOT NULL ORDER BY FechaHora DESC LIMIT 1"""
            mycursor.execute(sql)
            var = mycursor.fetchall()
            mydb.close()
        except:
            pass
        try:
            self.lastSendParada = var[0][1]
        except:
            #TODO fer el GET del WS
            self.lastSendParada = 0

    def saveRegParada(self):
        """Actualitzacio de lultm registre enviat
            S'ha de fer a la Base de dades taula lectura variable registro"""
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.pwd,
                database=self.dataBase)
            mycursor = mydb.cursor()
            # print(datetime.now(), self.EstadoLinea, self.nLinea, self.Procesadas, self.Buenas)
            sql = """INSERT INTO lectura (FechaHora, registroParadas) VALUES (%s,%s)"""
            mycursor.executemany(sql,[tuple([datetime.now(), self.lastSendParada])])

            sql = """DELETE FROM lectura WHERE registroParadas<'""" + str(self.lastSendParada-100000) + "'"
            mycursor.execute(sql)
            mydb.commit()

            mydb.commit()
            mydb.close()
        except Exception as e:
            print(e)
            f = open("managerDB.txt", "a")
            f.write(str(e) + ' \n')
            f.close()
            time.sleep(10)


    def deletePastParada(self):
            """Elimina tots els registres anteriors a les 24hors abans de la ultima enviada"""
            try:
                mydb = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.pwd,
                    database=self.dataBase)
                mycursor = mydb.cursor()
                sql = "DELETE FROM motivosParada WHERE NumeroRegistro < "+str(self.lastSendParada-10000)
                mycursor.execute(sql)
                mydb.commit()
                mydb.close()
            except Exception as e:
                print(e)
                f = open("managerDB.txt", "a")
                f.write(str(e) + ' \n')
                f.close()
                time.sleep(10)

    '''Enliminar de la base de dades trames antigues'''

    def postParada(self):
        notSend = []
        for ll in self.llistaParada:
            try:
                response = requests.post(self.urlParada, json=ll)
                print(response)
                if response.status_code == 200:
                    print(len(self.llistaParada), ll)
                    self.lastSendParada = ll['NumeroRegistro']
                    self.sendOkParada = False
                else:
                    notSend.append(ll)
            except Exception as e:
                print(e)
                f = open("managerDB.txt", "a")
                f.write(str(e) + ' send WS \n')
                f.close()
                notSend.append(ll)
                print('not post')
                # TODO intentar de reenviar les trames no transmeses

        if self.sendOkParada == False:
            self.saveRegParada()
            self.sendOkParada = True
            if not notSend:
                self.deletePastParada()

def readConfig():
    file = open("/home/root/config.json")
    dicConfig = json.load(file)
    file.close()
    return dicConfig


time.sleep(10)

dicConfig = readConfig()

mDB = mesbookDB(db=dicConfig['linea'], user='mesbook', pwd='123456789',
                host='localhost')

timeSend = datetime.now()
timeDelete = datetime.now()


while(True):
    try:
        if timeSend+timedelta(seconds=10) < datetime.now():
            mDB.readRegFisico()
            mDB.readRegParada()
            a = mDB.orderFisico(mDB.getFisico())
            b = mDB.orderParada(mDB.getParada())
            if a is not False:
                mDB.postFisico()
            if b is not False:
                mDB.postParada()
            timeSend = datetime.now()
        if timeDelete+timedelta(hours=1) < datetime.now():
            print('delete')
            timeDelete = datetime.now()
    except:
        print('Main error')
        time.sleep(10)


