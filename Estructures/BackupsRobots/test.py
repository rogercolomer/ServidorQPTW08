import json
from datetime import datetime

def getKeys():
    file = open("/home/root/BackupsRobots/machine.json")
    dicConfig = json.load(file)
    file.close()
    return dicConfig

a = getKeys()

query = ''
strin = ''
for r in a:
    query += r+','
    strin += '%s,'

sql = """INSERT INTO Robots ("""+query[:-1]+""") VALUES ("""+strin[:-1]+""")"""
# print(query[:-1])
# print(strin[:-1])
print(sql)
data = [datetime.now()]
