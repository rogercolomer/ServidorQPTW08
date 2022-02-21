import openpyxl
import json

from collections import OrderedDict
#
#
# def searchGama(dataJson,pOperacio):
#     for p in dataJson:
#         for o in p:
#             if len(o) == len(pOperacio):
#                 same = 0
#                 for c in o:
#                     if c in pOperacio:
#                         same += 1
#                 if same == len(pOperacio)+1:
#
#
#


dataList = []

book = openpyxl.load_workbook('/home/server/gamesQualitat/qualitatGesProf.xlsx')
sheet = book.active
for i in range(2, 6455):
    a = []
    c1 = "A" + str(i)
    c2 = "C" + str(i)
    c3 = "E" + str(i)
    a = [sheet[c1].value,sheet[c2].value,sheet[c3].value]
    dataList.append(a)

dataJson = {}


for d in dataList:
    for l in dataList:
        if l[0] == d[0]:
            if l[0] in dataJson:
                if l[1] in dataJson[l[0]]:
                    if l[2] not in dataJson[l[0]][l[1]]:
                        dataJson[l[0]][l[1]].append(l[2])
                else:
                    dataJson[l[0]][l[1]] = [l[2]]
            else:
                dataJson[l[0]] = {}
                dataJson[l[0]][l[1]] = [l[2]]
'''
Passem l'excel a un diccionari d'aquest format
"F45687":{"20":[control 1,control2],"40":[..]}
'''
controls = []
for p in dataJson:
    for ope in dataJson[p]:
        controls.append(tuple(sorted(dataJson[p][ope])))


final_list = list(OrderedDict.fromkeys(controls))   #elimininem controls duplicats

nControl = 0
dicControls = {}
for gama in final_list:
    dicControls[str(nControl)] = {}
    dicControls[str(nControl)]['gama'] = gama
    dicControls[str(nControl)]['producte'] = {}
    nControl += 1
"""
Diccionari de games
{'numControl': {'gama': ['control1','control2',..], producte : {producte1:'operacio1','producte2'...}}
"""

for control in dicControls:
    for p in dataJson:
        for o in dataJson[p]:
            if len(dicControls[control]['gama']) == len(dataJson[p][o]):
                contIgual = 0
                for c in dataJson[p][o]:
                    if c in dicControls[control]['gama']:
                        contIgual +=1
                print(dicControls[control]['gama'],dataJson[p][o],contIgual , len(dicControls[control]['gama']))
                if contIgual == len(dicControls[control]['gama']):
                    dicControls[control]['producte'][p] = o

print(dicControls)

jsonObject = json.dumps(dicControls)
print(jsonObject)
print(len(dicControls))