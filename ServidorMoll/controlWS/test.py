import time
import json
import requests
from datetime import datetime, timedelta
import mysql.connector


def getQPTW04():

    x = requests.get('http://147.45.45.3:85/GestProfWebService/Plan("",""true', timeout=60)
    dataJson = json.loads(x.text)
    for j in dataJson['result'][0]:
        x = requests.get('http://147.45.45.3:85/GestProfWebService/Plan("'+j['NumeroOrden']+'",""true', timeout=60)
        print(j['NumeroOrden'])

getQPTW04()

