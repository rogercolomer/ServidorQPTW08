import time
import numpy as np
import mysql.connector
import json
import snap7.client as c
from snap7.util import *
from datetime import datetime
from time import sleep

def deleteState():
    sql = """SELECT * FROM SeccionadorsGenerals ORDER BY timestamp DESC LIMIT 2"""
    mydb = mysql.connector.connect(
        host='192.100.101.40',
        user='consums',
        passwd='123456789',
        database='consums')
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    var = mycursor.fetchall()
    sql = "DELETE FROM SeccionadorsGenerals WHERE timestamp<'"+str(var[1][0])+"'"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()



deleteState()


