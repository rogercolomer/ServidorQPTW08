import mysql.connector
import time
import telebot
import numpy as np
import openpyxl
import sys
import threading
import json
from datetime import datetime
from datetime import timedelta

def getKeys():
    file = open("/home/roger/repositori/ServidorQPWood/Telegram/usersAlarmesProduccio.json")
    dicConfig = json.load(file)
    file.close()
    return dicConfig

chat_id = getKeys()



class Telegram:
    def __init__(self):
        self.numLines = self.inicialitzacioMaquines()

    def inicialitzacioMaquines(self):
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='mes',
            passwd='123456789',
            database='mes')
        sql = "SELECT numLine, line FROM numLines"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        values = mycursor.fetchall()
        mydb.close()
        dicLines = {}
        for v in values:
            if int(v[0])<10:
                dicLines['l00'+v[0]] = v[1]
            elif int(v[0])>=10 and int(v[0])<100:
                dicLines['l0' + v[0]] = v[1]
            elif int(v[0])>=100:
                dicLines['l' + v[0]] = v[1]
        return dicLines


    def readProd(self):
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='produccio',
            passwd='123456789',
            database='visualitzadorMesbook')
        sql = "SHOW TABLES"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        values = mycursor.fetchall()

        sql = "SELECT * FROM telegramExces"
        mycursor.execute(sql)
        sendMes = mycursor.fetchall()
        dicExces = {}
        for sm in sendMes:
            dicExces[sm[2]] = sm[1]


        sql = "SELECT * FROM telegramMarcha"
        mycursor.execute(sql)
        marchaMes = mycursor.fetchall()
        dicMarcha = {}

        for marcha in marchaMes:
            dicMarcha[marcha[1]] = marcha[0]
        print(dicMarcha)
        for v in values:
            if v[0] != 'telegramExces' and v[0] != 'telegramMarcha':
                #Acces de produccio
                sql = "SELECT * FROM "+v[0]
                mycursor.execute(sql)
                data = mycursor.fetchall()
                if data != []:
                    if not v[0] in dicExces:
                        print(data,v)
                        if data[0][14] > 105.0:
                            sql = """INSERT INTO telegramExces (timestamp, NumeroOrden, linea) VALUES (%s,%s,%s)"""
                            dada = [datetime.now(), data[0][1],v[0]]
                            mycursor.executemany(sql, [tuple(dada)])
                            mydb.commit()

                            missatge = '*Excés producció*: \n' \
                                        '    Línea: '+str(self.numLines[v[0]])+'\n' \
                                        '    OF: '+str(dada[1])+'\n'\
                                        '    Codi: '+data[0][2]
                            self.tb = telebot.TeleBot(token)
                            self.sendMissatge(missatge)
                            self.tb.stop_bot()
                    elif v[0] in dicExces:
                        if dicExces[v[0]] != data[0][1]:
                            sql = "DELETE FROM telegramExces WHERE linea = '"+v[0]+"'"
                            mycursor.execute(sql)
                            mydb.commit()

                    if not v[0] in dicMarcha:
                        sql = """INSERT INTO telegramMarcha (NumeroOrden, linea) VALUES (%s,%s)"""
                        dada = [data[0][1], v[0]]
                        mycursor.executemany(sql, [tuple(dada)])
                        mydb.commit()
                        missatge = '▶️ *Marxa*: \n' \
                                   '      Línea: ' + str(self.numLines[v[0]]) + '\n' \
                                   '      OF: ' + str(data[0][1]) + '\n' \
                                   '      Codi: ' + \
                                   data[0][2]
                        self.tb = telebot.TeleBot(token)
                        self.sendMissatge(missatge)
                        self.tb.stop_bot()
                elif v[0] in dicMarcha:
                    sql = "DELETE FROM telegramMarcha WHERE linea = '"+v[0]+"'"
                    print(sql)
                    mycursor.execute(sql)
                    mydb.commit()
                    missatge = '*🛑 Parada*: \n' \
                                '      Línea: ' + str(self.numLines[v[0]]) + '\n' \
                                '      OF: ' + str(dicMarcha[v[0]])
                    self.tb = telebot.TeleBot(token)
                    self.sendMissatge(missatge)
                    self.tb.stop_bot()
                # else:
                #     sql = "DELETE FROM telegramMarcha WHERE linea = '" + v[0] + "'"
                #     print(sql)
                #     mycursor.execute(sql)
                #     mydb.commit()

        mydb.close()

    def sendMissatge(self,m):
        # c = '743717839'
        # self.tb.send_message(c, text=str(m), parse_mode="Markdown")
        # # print(c + ' :' + str(m))

        for c in chat_id:
            try:
                self.tb.send_message(c, text=str(m), parse_mode="Markdown")
                print(c + ' :' + str(m))
            except:
                pass



"""https://api.telegram.org/bot867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs/getUpdates"""
token = '867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs'



t = Telegram()
while(True):
    try:
        t.readProd()
        time.sleep(10)
    except Exception as e:
        print(e)
# readProd()
