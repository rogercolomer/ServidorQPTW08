import time
import snap7.client as c
import mraa
from datetime import datetime
import mysql.connector

def save_data(data,sql):
    '''
    :param data: list dels objectes insertar a la sql
    :param sql: query sql
    :return: None
    '''
    try:
        data.insert(0, datetime.now())

        mydb = mysql.connector.connect(
            host= '192.100.101.40',
            user='compressors',
            passwd='123456789',
            database='compressors')
        mycursor = mydb.cursor()
        mycursor.executemany(sql, [tuple(data)])
        mydb.commit()
        mydb.close()
    except:
        print('error')

def readPLC():
    '''
    :return: estat dels compressors [r125, r125V i r100]
    '''
    try:
        plc = c.Client()
        plc.connect('192.100.101.36', 0, 1)  # ip
        value = plc.db_read(1, 0, 1)  # llegir db (numero_db,primer byte, longitud maxima)
        print(value[:],type(value))
        estat = "{0:b}".format(int.from_bytes([0, value[0]], byteorder='big', signed=False))
        plc.disconnect()
        plc.destroy()
        # omplim la string fins a 6 caràcters amb 0's perque sinos esfa mes curta quan ek r125V és 0
        while (len(estat) < 6):
            estat = '0' + estat
        r125 = int(estat[3])
        r125V = int(estat[0])
        r100 = 0
        return [r125, r125V, r100]
    except:
        print('error')
        return [2, 2, 2]

def setState(func):
    b = func.to_bytes(1, 'big')
    print(b[0])
    plc = c.Client()
    plc.connect('192.100.101.36', 0, 1)  # ip
    plc.db_write(1, 0, b)
    plc.disconnect()
    plc.destroy()

sqlSensor = """INSERT INTO comp_sen(timestamp, pres) VALUES (%s, %s)"""
sqlEstat = """INSERT INTO estat(timestamp, r125, r125V, r100) VALUES (%s, %s, %s, %s)"""
IOShield_U0 = mraa.Aio(0) # Analog Input
flag = 0

while(True):
    try:
        save_data(readPLC(),sqlEstat)
        value_U0 = (IOShield_U0.read() * 10) / 1023  # read the value of U0
        save_data([value_U0],sqlSensor)
        time.sleep(5)
        print('ok')
    except KeyboardInterrupt:
        raise
    except:
        print('error')

    if datetime.now().weekday() == 0:
        if datetime.now().hour == 12:
            if flag == 0:
                setState(36)
                flag = 1
                print('done ')
        elif datetime.now().hour == 23:
            flag = 0
    if datetime.now().weekday() == 5:
        if datetime.now().hour == 2:
            if flag == 0:
                setState(0)
                flag = 1
        elif datetime.now().hour == 3:
            flag = 0
    if datetime.now().weekday() == 5:
        if datetime.now().hour == 6:
            if flag == 0:
                setState(32)
                flag = 1
        elif datetime.now().hour == 7:
            flag = 0
    if datetime.now().weekday() == 5:
        if datetime.now().hour == 18:
            if flag == 0:
                setState(0)
                flag = 1
        elif datetime.now().hour == 19:
            flag = 0


# """
# dia 4 a les 22:00 parada del compressor 1 (es queda en marxa el 2)
# dia 5 a les 02:00 parada dels compressors
# dia 5 a les 06:00 encesa del compresosr 2
# dia 5 a les 18:00 parada dels compressors
# """