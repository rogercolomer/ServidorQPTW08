import time
import telebot
import mysql.connector
import json
import os
import subprocess
import openpyxl
from telebot import types
from datetime import datetime

def getKeys():
    file = open("/home/roger/repositori/ServidorQPWood/Telegram/usersBot.json")
    dicConfig = json.load(file)
    file.close()
    return dicConfig

chat_id = getKeys()

# https://api.telegram.org/bot867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs/getUpdates
token = '867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs'
# chat_id = ['743717839', '815134963',  '1387210673', '1259688712', '1394582515', '409835547', '1772890260','2103459791','2103459926','857156986']
try:
    tb = telebot.TeleBot(token)
    print('ok')
except:
    print('error iniciacio')

time.sleep(10)



@tb.message_handler(commands=['OTR'])
def Otr(message):
    try:
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='telegram',
            passwd='123456789',
            database='OTR')
        if mydb.is_connected():
            mycursor = mydb.cursor()
            sql = "SELECT timestamp,Estat_OTR,Feedback_V101,V402,V404,V406,V408,TE107,Pot_cremador FROM data ORDER BY timestamp DESC LIMIT 1"
            mycursor.execute(sql)
            records = mycursor.fetchall()
            mydb.close()

            if records[0][1] == 1:
                m1 = 'Seguretat'
            elif records[0][1] == 2:
                m1 = 'Repos'
            elif records[0][1] == 3:
                m1 = 'Purga'
            elif records[0][1] == 4:
                m1 = 'Escalfament'
            elif records[0][1] == 5:
                m1 = 'Commutacio'
            elif records[0][1] == 6:
                m1 = 'Estandar'
            elif records[0][1] == 7:
                m1 = 'Parada'
            elif records[0][1] == 8:
                m1 = 'Refredament'
            elif records[0][1] == 9:
                m1 = 'Paro variadors'
            elif records[0][1] == 10:
                m1 = 'Standby'

            if records[0][3] == 2 or records[0][4] == 2 or records[0][5] == 2 or records[0][6] == 2:
                m2 = 'La maquina no esta funcionant correctament'
            elif records[0][3] == 4 or records[0][4] == 4 or records[0][5] == 4 or records[0][6] == 4:
                m2 = 'La maquina està operativa'
            m3 = 'El motor està treballant al ' + str(records[0][2]) + ' %'
            m4 = 'Temperatura càmera ' + str(records[0][7]) + ' ºC'
            m5 = 'Potència cremador '+str(records[0][8])+' %'
            data = 'Hora : ' + str(records[0][0])
            m = '*🔥 OTR*: \n' + data + '\nEstat: ' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4 + '\n' + m5
            enviar_missatge(message.chat.id, m)

            mycursor.close()
            mydb.close()
            time.sleep(5)
        else:
            print('caca')
    except:
        print('error OTR')


@tb.message_handler(commands=['AlarmesAspiracio'])
def AlarmesAspriacio(message):
    try:
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='aspiracio',
            passwd='123456789',
            database='aspiracio')

        sql = "SELECT * FROM alarma"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        values = mycursor.fetchall()

        mydb.close()
        if values != []:
            m = "🏭* Alarmes Aspiracio*: \n"
            for i in values:
                m += i[1] + " \n"
            enviar_missatge(message.chat.id, m)
    except:
        print('error AlarmesAspiracio')



@tb.message_handler(commands=['Compressor'])
def Comp(message):
    # m = 'Funció no operativa en aquets moments'
    # enviar_missatge(message.chat.id, m)
    try:
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='telegram',
            passwd='123456789',
            database='compressors')
        if mydb.is_connected():
            mycursor = mydb.cursor()
            sql = "SELECT timestamp,pres FROM comp_sen ORDER BY timestamp DESC LIMIT 1"
            mycursor.execute(sql)
            records = mycursor.fetchall()
            mydb.close()
            # print(records[0])
            print(records)
            if records == []:
                m = "No hi ha data"
            else:
                m = '💨 *Compressors*: \nLa pressió és de '+str(records[0][1])+' bars'
            enviar_missatge(message.chat.id, m)
    except:
        print('error Compressor')


@tb.message_handler(commands=['EspurnesAspiracio'])
def Espurnes(message):
    pass


@tb.message_handler(commands=['ArrencadorsAspiracio'])
def Arrencadors(message):
    try:
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='telegram',
            passwd='123456789',
            database='aspiracio')

        if mydb.is_connected():
            mycursor = mydb.cursor()
            sql = "SELECT timestamp,Consum_L01,Consum_L02,Consum_L03,Consum_L04,Consum_L05,Consum_L06,Consum_L07,Consum_L08,Consum_L11,Consum_L13 FROM consums ORDER BY timestamp DESC LIMIT 1"
            mycursor.execute(sql)
            records = mycursor.fetchall()
            mydb.close()
        m = '🏭* Aspiracio*' + '\n' + 'L-01: ' + str(
            round(records[0][1], 2)) + ' A' + '\n' + 'L-02: ' + str(
            round(records[0][2], 2)) + ' A' + '\n' + 'L-03: ' + str(
            round(records[0][3], 2)) + ' A' + '\n' + 'L-04: ' + str(
            round(records[0][4], 2)) + ' A' + '\n' + 'L-05: ' + str(
            round(records[0][5], 2)) + ' A' + '\n' + 'L-06: ' + str(
            round(records[0][6], 2)) + ' A' + '\n' + 'L-07: ' + str(
            round(records[0][7], 2)) + ' A' + '\n' + 'L-08: ' + str(
            round(records[0][8], 2)) + ' A' + '\n' + 'Impulsió: ' + str(
            round(records[0][9], 2)) + ' A' + '\n' + 'General: ' + str(round(records[0][10], 2)) + ' A'
        enviar_missatge(message.chat.id, m)

        time.sleep(5)
    except:
        print('error Arrencadors Aspiracio')


@tb.message_handler(commands=['Biomassa'])
def Biomassa(message):
    try:
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='biomassa',
            passwd='123456789',
            database='biomassa')

        sql = "SELECT * FROM estatTemp ORDER BY timestamp DESC LIMIT 1"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        values = mycursor.fetchall()

        sql = "SHOW FIELDS FROM estatTemp"
        mycursor.execute(sql)
        fields = mycursor.fetchall()
        data = {}
        count = 0
        for f in fields:
            data[f[0]] = values[0][count]
            count += 1
        mydb.close()

        m = "🌲 *Biomassa*: \n" \
            "Hora: " + str(data['timestamp']) + '\n' \
            "Temp Bio 1: " + str(data['TCTR_106_INT_MCB1_ME_TSOR_AIGUA']) + ' ºC\n' \
            "Temp Cam 1: " + str(data['TCTR_106_INT_MCB1_ME_TCOM_CAMBRE']) + ' ºC\n' \
            "Temp Bio 2: " + str(data['TCTR_106_INT_MCB2_ME_TSOR_AIGUA']) + ' ºC\n' \
            "Temp Cam 2: " + str(data['TCTR_106_INT_MCB2_ME_TCOM_CAMBRE']) + ' ºC\n' \
            "Temp Pri: " + str(data['TCTR_100_ME_TDEP_90_ALT']) + ' ºC (' + str(data['TCTR_100_XS_TEMP_CALOR_DIPOSIT']) + ' ºC)\n' \
            "Temp Sec: " + str(data['TCTR_100_ME_TDEP_80_ALT']) + ' ºC (' + str(data['TCTR_100_XS_DIP_CALOR_SEC']) + ' ºC)\n' \
            "Temp Fred: " + str(data['TCTR_101_ME_TDEP_7_ALT']) + ' ºC (' + str(data['TCTR_106_INT_MABS_ME_XSREFEDA']) + ' ºC)\n' \
            "Temp Gas 1: " + str(data['TCTR_100_ME_TIMP_ST17_CAS1']) + ' ºC\n' \
            "Temp Gas 2: " + str(data['TCTR_100_ME_TIMP_ST16_CAS2']) + ' ºC\n'
        enviar_missatge(message.chat.id, m)
    except:
        print('error Biomassa')


@tb.message_handler(commands=['AlarmesBiomassa'])
def alarmesBiomassa(message):
    try:
        mydb = mysql.connector.connect(
            host='192.100.101.40',
            user='biomassa',
            passwd='123456789',
            database='biomassa')

        sql = "SELECT * FROM alarmes"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        values = mycursor.fetchall()

        mydb.close()
        if values != []:
            m = "🌲 *Alarmes Biomassa*: \n"
            for i in values:
                m += i[2]+" \n"
            enviar_missatge(message.chat.id, m)
    except:
        print('error AlarmesBiomassa')

def enviar_missatge(idtelebot, missatge):
    for i in chat_id:
        if str(idtelebot) == i:
            print(str(datetime.now()) + ' , ' + str(idtelebot))
            tb.send_message(str(idtelebot), text=str(missatge), parse_mode="Markdown")

@tb.message_handler(commands=['start'])
def Start(message):
    try:
        infoUser = str(message.from_user)
        print(message)
        # iU2 =infoUser.replace("'",'"')
        # print(iU2)
        # infoJson = json.loads(iU2)
        # print(infoJson,type(infoJson))
        # missatge = infoJson['first_name']+' '+infoJson['last_name']+'\n'
        # missatge += infoJson['id']
        # print(missatge)
        # # missatge = ""
        tb.send_message("743717839", text=str(infoUser), parse_mode="Markdown")
    except:
        print('error Start')

error_counter = 0
markup = types.ReplyKeyboardMarkup(row_width=1)
b1 = types.KeyboardButton('/AlarmesAspiracio')
b2 = types.KeyboardButton('/OTR')
b3 = types.KeyboardButton('/ArrencadorsAspiracio')
b4 = types.KeyboardButton('/Compressor')
b5 = types.KeyboardButton('/Biomassa')
b6 = types.KeyboardButton('/AlarmesBiomassa')
b7 = types.KeyboardButton('/')
b8 = types.KeyboardButton('/')
markup.add(b3, b2, b4, b1, b5, b6) #, b5, b6, b7, b8)

# for c in chat_id:
#     try:
#         tb.send_message(c, 'Actualització del bot ⏳ - Alarmes biomassa ', reply_markup=markup)
#     except:
#         print(c)
# tb.send_message('857156986', 'Actualització del bot + biomassa)', reply_markup=markup)
# tb.send_message('409835547', 'Botons', reply_markup=markup)


# book = openpyxl.load_workbook('/home/user/Telegram/Alarmes_telegram_socket.xlsx')
# sheet = book.active
# dic = {}
# for i in range(2,233):
#     c1 = "B"+str(i)
#     c2 = "C"+str(i)
#     dic[sheet[c1].value] = sheet[c2].value

print('polling', datetime.now())
while(True):
    try:
        tb.polling(none_stop=True, interval=0, timeout=60)
    except KeyboardInterrupt:
        raise
    except:
        print('error')




