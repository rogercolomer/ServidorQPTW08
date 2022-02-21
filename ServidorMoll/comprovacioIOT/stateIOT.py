# source yourenv/bin/activate s'ha dexecutar amb el python3.8
from pexpect import pxssh
from datetime import datetime, timedelta
import time
import json
import mysql.connector


class State:
    def __init__(self, ip, name, script, user, password):

        self.ip = str(ip)
        self.name = str(name)
        self.script = script
        self.user = user
        self.password = password

        self.connection = None
        self.date = None

    def setState(self, a):
        self.connection = a

    def connectIOT(self):
        try:
            s = pxssh.pxssh(timeout=4)
            s.login(self.ip, self.user, self.password,sync_multiplier=5, auto_prompt_reset=False)
            s.sendline('ps -ef|grep python')
            s.prompt()
            a = s.before.decode('utf-8')
            # print(a)
            # print(s.logout())
            run = 0
            for scr in self.script:
                if a.find(scr) > 0:
                    run += 1
                else:
                    pass
            if run == len(self.script):
                self.setState(2)
            else:
                self.setState(1)
        except Exception as e:
            print(e)
            if str(e) == 'Could not establish connection to host':
                self.setState(0)
            else:
                print(str(e))
                self.setState(3)

    def saveState(self,line, db, cursor):
        print( line +' '+str(self.connection))
        sql = "INSERT INTO "+line+" (timestamp,connect) VALUES (%s, %s)"
        # print(tuple([datetime.now(), self.connection]))
        cursor.executemany(sql, [tuple([datetime.now(), self.connection])])
        db.commit()

    def __str__(self):
        return str(self.name)+" - "+str(self.connection)


class StateLines:
    def __init__(self):
        self.dicState = {}
        file = open("/home/server/comprovacioIOT/lines.json")
        lines = json.load(file)
        file.close()
        for l in lines:
            # print(lines[l]['ip'], lines[l]['name'], lines[l]['script'], lines[l]['user'], lines[l]['password'])
            self.dicState[l] = State(ip=lines[l]['ip'],
                                     name=lines[l]['name'],
                                     script=lines[l]['script'],
                                     user=lines[l]['user'],
                                     password=lines[l]['password'])

    def generalSatus(self):
        for d in self.dicState:
            self.dicState[d].connectIOT()
            print(self.dicState[d])
        self.saveStatus()

    def saveStatus(self):
        print('hola',self.dicState)
        mydb = mysql.connector.connect(
            host='localhost',
            user='stateIOT',
            passwd='123456789',
            database='stateIOT')
        mycursor = mydb.cursor()
        for d in self.dicState:
            self.dicState[d].saveState(d, mydb, mycursor)
        mydb.close()


s = StateLines()
s.generalSatus()
