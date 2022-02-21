import requests
import time
import mysql.connector
from datetime import datetime

print('     Execute consums: '+str(datetime.now()))
urls = ['http://147.45.45.3:22222/services/user/values.xml?var=General.API?...?id=General?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=Bloc%20Tecnic.API?...?id=Bloc%20Tecnic?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=Aspiració.API?...?id=Aspiració?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=Compressors.API?...?id=Compressors?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=Pintura%20-%20OTR%20-%20QPIM.API?...?id=Pintura%20-%20OTR%20-%20QPIM?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=Magatzem%20TDM.API?...?id=Magatzem%20TDM?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=Biomassa.API?...?id=Biomassa?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=OTR%20(PINTURA).API?...?id=OTR%20(PINTURA)?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=QPIM%20(PINTURA).API?...?id=QPIM%20(PINTURA)?...',
        'http://147.45.45.3:22222/services/user/values.xml?var=TWP02-2A+2B+2C.API?...?id=TWP02-2A+2B+2C',
        'http://147.45.45.3:22222/services/user/values.xml?var=TWP01-1A+1B.API?...?id=TWP01-1A+1B?...']
seccions = ['General', 'Bloc tecnic', 'Aspiracio', 'Compressors', 'Pinutra general', 'Magatzem',
            'Biomassa', 'OTR', 'Pintura','TWP02-2A+2B+2C','TWP01-1A+1B']
valors = {'General': 0.0,
          'Bloc tecnic': 0.0,
          'Aspiracio': 0.0,
          'Compressors': 0.0,
          'Pinutra general': 0.0,
          'Magatzem': 0.0,
          'Biomassa': 0.0,
          'OTR': 0.0,
          'Pintura': 0.0,
          'TWP02-2A+2B+2C':0.0,
          'TWP01-1A+1B':0.0}
n = 0
for url in urls:
    s = requests.Session()
    data = s.get(url).text
    api = data.find('API') + 15
    val = ''
    for i in range(5):
        val += data[api + i]
    valors[seccions[n]] = float(val)
    n += 1
    s.close()

print(valors)
mydb = mysql.connector.connect(
        host='192.100.101.40',
        user='consums',
        passwd='123456789',
        database='consums')

mycursor = mydb.cursor()
sql = """INSERT INTO potencia (timestamp, general, BlocTecnic, Aspiracio, Compressors, PinturaGeneral, Magatzem, Biomassa, OTR, Pintura,TWP01, TWP02) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
v = [datetime.now(), valors['General'], valors['Bloc tecnic'], valors['Aspiracio'], valors['Compressors'],
     valors['Pinutra general'], valors['Magatzem'], valors['Biomassa'], valors['OTR'], valors['Pintura'],
     valors['TWP02-2A+2B+2C'],valors['TWP01-1A+1B']]
mycursor.executemany(sql, [tuple(v)])
mydb.commit()
mydb.close()
