import mysql.connector
from datetime import datetime,timedelta

def deleteFisico(config):

    mydb = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        passwd=config['passwd'],
        database=config['database'])
    mycursor = mydb.cursor()
    sql = """DELETE FROM productividad_productividad WHERE FechaHora<'""" + str(datetime.now()-timedelta(days=7)) + "'"
    mycursor.execute(sql)
    print(sql)
    mydb.commit()
    mydb.close()
    print('done fisico')

def deleteMotivosParada(config):

    mydb = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        passwd=config['passwd'],
        database=config['database'])
    mycursor = mydb.cursor()
    sql = """DELETE FROM motivosparada_motivosparada WHERE FechaHoraFin<'""" + str(datetime.now()-timedelta(days=7)) + "'"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    print('done paradas')

def deleteMovimientosTiempoReal(config):
    mydb = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        passwd=config['passwd'],
        database=config['database'])
    mycursor = mydb.cursor()
    sql = """DELETE FROM movimientostiemporeal_movimientostiemporeal WHERE TimeStamp<'""" + str(
        datetime.now() - timedelta(days=7)) + "'"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
    print('done movimientos')


config =   {'host': '147.45.45.4',
            'user': 'control',
            'passwd': '123456789',
            'database': 'fisico'}

deleteFisico(config)
deleteMotivosParada(config)
deleteMovimientosTiempoReal(config)
print('     Correct')