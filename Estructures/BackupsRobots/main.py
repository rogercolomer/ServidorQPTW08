import tarfile
import os
import json
import mysql.connector
from ftplib import FTP
from datetime import datetime

'''
.tar.gz
tar -czvf ROB03.tar.gz ROB03/
$ tar -xzvf file.tar.gz

'''

def insertDatabase(jsonRobots, jsonState):
    query = 'timestamp,'
    strin = '%s,'
    data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    for r in jsonRobots:
        query += r + ','
        strin += '%s,'
        data.append(jsonState[r])

    sql = """INSERT INTO Robots (""" + query[:-1] + """) VALUES (""" + strin[:-1] + """)"""
    print(sql)
    mydb = mysql.connector.connect(
        host='192.100.101.40',
        user='stateIOT',
        passwd='123456789',
        database='stateIOT')
    mycursor = mydb.cursor()
    mycursor.executemany(sql, [tuple(data)])
    mydb.commit()
    mydb.close()

def getJson():
    file = open("/home/root/BackupsRobots/machine.json")
    dicConfig = json.load(file)
    file.close()
    return dicConfig


def makeTarfile(outputFilename, sourceDir):
    with tarfile.open(outputFilename, "w:gz") as tar:
        tar.add(sourceDir, arcname=os.path.basename(sourceDir))


robots = getJson()
data = datetime.now()
estatBackup = {}

for r in robots:
    try:
        ftp = FTP(robots[r])
        files = ftp.nlst()
        os.mkdir('/home/root/BackupsRobots/' + r)
        for f in files:
            with open('/home/root/BackupsRobots/'+r+'/'+f, 'wb') as fp:
                ftp.retrbinary('RETR '+f, fp.write)
        makeTarfile('/home/root/BackupsRobots/backups/'+r+'_'+data.strftime("%Y%m%d")+'.tar.gz', '/home/root/BackupsRobots/'+r)
        os.system("cp /home/root/BackupsRobots/backups/"+r+"_"+data.strftime('%Y%m%d')+".tar.gz /mnt/Robots/"+r)
        ftp.quit()
        if os.path.exists('/home/root/BackupsRobots/'+r):
            # removing the file using the os.remove() method
            os.system('rm -r /home/root/BackupsRobots/'+r)
            print('Done: '+r)
            estatBackup[r] = 1
        else:
            # file not found message
            print("File not found in the directory")
            estatBackup[r] = 0
    except:
        print('Error: '+r)
        estatBackup[r] = 0

insertDatabase(robots,estatBackup)