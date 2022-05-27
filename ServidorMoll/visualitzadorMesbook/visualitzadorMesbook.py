from datetime import datetime, timedelta
import time
import json
import mysql.connector
import pymssql
import string
# try:
file = open("/home/server/visualitzadorMesbook/numLiniesNom.json")
lines = json.load(file)
file.close()

conn = pymssql.connect('192.100.50.20', 'consultaOF', 'QP_consulta12', "Mesbook")
print(conn)
cursor = conn.cursor()
cursor.execute("""SELECT NumeroOrden, Codigo, Inicio, Linea, Estado, CantidadOf, CantidadProcesada, CantidadBuena,
                    PersonalObj, PersonalAsignadoReal, ControlesPendientesProduccion , ControlesPendientesCalidad,
                    AveriasSinReportar, Scrap FROM ConsultaOFs_EnCurso;""")
# cursor.execute("""SELECT COLUMNS FROM ConsultaOFs_EnCurso;""")
hora = datetime.now()
mydb = mysql.connector.connect(
            host='localhost',
            user='visualitzadorLocal',
            passwd='123456789',
            database='visualitzadorMesbook')
mycursor = mydb.cursor()

for row in cursor:
    a = list(row)
    a.append(hora)
    #determinar estat de maquina com a int 1 marcha 0 paro
    if row[4]=='Pausa':
        estat = 0
    elif row[4]=='Marcha' or row[4]=='ArranqueAdministrativa':
        estat = 1
    else:
        estat = 0
    a.append(estat)
    # Convertim les OF a números eliminant tots els altres simbols
    # of = ''
    # for i in a[0]:
    #     if string.digits.find(i) != -1:
    #         of += i
    # if of == '':
    #     a[0] = 9999
    # else:
    #     a[0] = of
    try:
        a.append((int(a[7])/int(a[5]))*100)
    except:
        a.append(None)
    if estat == 1:
        try:
            sql = """INSERT INTO """+str(lines[a[3]])+""" (NumeroOrden, Codigo, Inicio, CantidadOf, CantidadProcesada, CantidadBuena,
                                PersonalObj, PersonalAsignadoReal, ControlesPendientesProduccion , ControlesPendientesCalidad,
                                AveriasSinReportar, Scrap, timestamp, Estado,percentProd)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            a.pop(3)
            a.pop(3)
            mycursor.executemany(sql, [tuple(a)])
            print(row)
        except:
            print('error al ffer lincert')

# try:
conn.close()
mydb.commit()
# except:
#     print('commit')

# try:
for l in lines:
    sql = "DELETE FROM "+lines[l]+" WHERE timestamp < '" + hora.strftime('%Y/%m/%d %H:%M:%S') + "'"
    print(l)
    mycursor.execute(sql)

mydb.commit()
mydb.close()
# except:
#     print('delete')
