import time
import snap7.client as c
import mraa
from datetime import datetime
import mysql.connector
import ctypes

a = 32
b = a.to_bytes(1,'big')
print(b[0])
flag = 0

plc = c.Client()
plc.connect('192.100.101.36', 0, 1)  # ip
value = plc.db_read(1, 0, 1)  # llegir db (numero_db,primer byte, longitud maxima)
plc.db_write(1,0,b)
plc.disconnect()
plc.destroy()

# if datetime.now().day == 4:
#     if datetime.now().hour == 22:
#         if flag == 0:
#             setState(32)
#             flag = 1
#     elif datetime.now().hour == 23:
#         flag = 0
# if datetime.now().day == 5:
#     if datetime.now().hour == 2:
#         if flag == 0:
#             setState(0)
#             flag = 1
#     elif datetime.now().hour == 3:
#         flag = 0
# if datetime.now().day == 5:
#     if datetime.now().hour == 6:
#         if flag == 0:
#             setState(32)
#             flag = 1
#     elif datetime.now().hour == 7:
#         flag = 0

while True:
    if datetime.now().weekday() == 1 and (datetime.now().hour == 9 and datetime.now().hour<10):
        print(datetime.now(), 'dins')
    else:
        print('fora')
    time.sleep(200)

'''
0 tot parat 
4 compressor 1 en marxa
32 compressor 2 en marxa 
36 tots en marxa 
'''

''' 
dia 4 a les 22:00 parada del compressor 1 (es queda en marxa el 2)
dia 5 a les 02:00 parada dels compressors
dia 5 a les 06:00 encesa del compresosr 2
dia 5 a les 18:00 parada dels compressors 


'''