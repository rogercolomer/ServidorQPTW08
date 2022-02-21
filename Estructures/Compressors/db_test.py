import sqlite3
from datetime import datetime
import time
import django

table = 'maquina'
database = 'produccio.db'
def inset_sqlite(v):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    v[0]= v[0].strftime("%m-%d-%Y, %H:%M:%S")
    c.execute("INSERT INTO "+table+" VALUES (?,?,?,?,?)", tuple(v))
    conn.commit()
    c.close()
    conn.close()

def delete_sqlite(date):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("DELETE FROM "+table+" WHERE datetime<'"+date.strftime("%m-%d-%Y, %H:%M:%S")+"'")
    conn.commit()
    c.close()
    conn.close()

def createTable_sqlite():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("CREATE TABLE "+table+" (datetime text, pIn int, pOut int, state int, a0 int)")
    c.close()
    conn.close()

def select_sqlite(date):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM "+table+" WHERE datetime<'"+date.strftime("%m-%d-%Y, %H:%M:%S")+"'")
    records = c.fetchall()
    c.close()
    conn.close()
    return records


sFifo = 1
createTable_sqlite()
sDate = datetime.now()
# delete_sqlite(sDate)
for i in range(100):
    data = [datetime.now(),500+i,504+i,1,0]
    inset_sqlite(data)
    time.sleep(1)

print(select_sqlite(datetime.now()))

#TODO main program for redundat data

# if sFifo == 0:
#     try:
#         print('Send data')
#     except:
#         sDate = datetime.now()
#         sFifo = 1
#         print('Active FIFO')
#
# else:
#     print('get all data no send ',sDate)
#     try:
#         print('Send data')
#         sFifo = 0
#     except:
#         pass
#
# try:
#     print('Save SQLite')
# except:
#     print('Liada parda')