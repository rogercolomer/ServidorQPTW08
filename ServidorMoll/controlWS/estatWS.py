# import time
# import json
# import requests
# from datetime import datetime, timedelta
# import mysql.connector
#
#
# def saveDB(table, estat):
#     mydb = mysql.connector.connect(
#         host='localhost',
#         user='roger',
#         passwd='123456789',
#         database='monitorWS')
#     mycursor = mydb.cursor()
#     sql = """INSERT INTO """ + table + """ (FechaHora, state) VALUES (%s,%s)"""
#     mycursor.execute(sql, tuple([datetime.now(), estat]))
#     mydb.commit()
#     sql = """DELETE FROM """ + table + """ WHERE FechaHora<'""" + str(datetime.now() - timedelta(days=7)) + "'"
#     mycursor.execute(sql)
#     mydb.commit()
#     mydb.close()
#
#
# def getQPTW05():
#     FechaHora = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#     try:
#         x = requests.get('http://147.45.45.4:8000/api/fisico/' + FechaHora)
#         if x.status_code == 200:
#             estat = 1
#         else:
#             estat = 0
#     except:
#         estat = 0
#     return estat
#
#
# def getQPTW04():
#     x, dataJson = None, None
#     try:
#         x = requests.get('http://147.45.45.3:85/GestProfWebService/Plan("",""true', timeout=60)
#         dataJson = json.loads(x.text)
#     except:
#         pass
#     mydb = mysql.connector.connect(
#         host='localhost',
#         user='roger',
#         passwd='123456789',
#         database='monitorWS')
#     mycursor = mydb.cursor()
#     sql = """DELETE FROM velocitatZero WHERE timestamp<'""" + str(datetime.now() - timedelta(minutes=10)) + "'"
#     mycursor.execute(sql)
#     mydb.commit()
#     mydb.close()
#     try:
#         if x.text.find('FechaPrefFabricacion') != -1:
#             estat = 1
#         elif dataJson['result'] == [None]:
#             estat = 1
#         else:
#             estat = 0
#     except:
#         estat = 0
#     print('estat ',estat)
#     return estat
#
#
# saveDB("state", getQPTW05())
# saveDB("qptw04", getQPTW04())
