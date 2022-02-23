import snap7.client as c
from random import randint
import os
import mraa
try:
    import usb.core
    import usb.util
    import sys
    import time
    import struct
    import json
except:
    print('Error import USB')


""" 
    Mòdul Python creat per les comunicacions amb les màquines de TWP 
    utilitzant els dispositius IOT2040
    Classes: Comunication, USB(Comunication), Modbus (Comunication), S7 (Comunication) ,UART (Comunication)
    SF: UinDuint
    Python3
    Autor: Roger Colomer 
    Data de creació : 07/04/2020
    Modicifacio : 15/4/2020
"""


def UintDuint(c0, c1):
    s0 = hex(c0)[2:len(hex(c0))]  # concatenem els dos parells de bytes en 4 bytes junts per fer una DUINT
    s1 = hex(c1)[2:len(hex(c1))]
    # omplim les string amb 0's peque es puguin concatenar (4 valors hex cada una )
    # quan es concatenin tindran 8 valors hex que són 32 bits
    while len(s0) < 4:
        s0 = '0' + s0
    while len(s1) < 4:
        s1 = '0' + s1
    t = (s1 + s0)
    return int(t, 16)


class Comunication:
    def __init__(self, v):  # ordre variables, longitud lectura
        self.variables = v
        self.len0 = self.get_len()

        self.data = []
        self.dataA = []
        self.dataB = 'b'

    def get_len(self):
        l = 0
        for v in self.variables:
            if v[2] == 1:
                l += v[1]
        return l

    def makeArray(self):
        pos = 0
        self.dataA = []
        for var in self.variables:
            if var[2] == 1:  # ha destar plena
                if var[1] == 1:  # 2 bytes
                    self.dataA.append(self.data[pos])
                    pos += 1
                elif var[1] == 2:  # 4 bytes
                    self.dataA.append(UintDuint(self.data[pos], self.data[pos + 1]))
                    pos += 2
                else:
                    print('el valor no és ni 1 ni 2')
            elif var[2] == 0:
                if var[1] == 1:  # 2 bytes
                    self.dataA.append(0)
                elif var[1] == 2:  # 4 bytes
                    self.dataA.append(0)
                else:
                    print('el valor no és ni 1 ni 2')

    def makeBytes(self):
        self.dataB = b''
        pos = 0
        for var in self.variables:
            if var[1] == 1:  # 2 bytes
                self.dataB += (self.dataA[pos]).to_bytes(2, byteorder='big')
            elif var[1] == 2:  # 4 bytes
                self.dataB += (self.dataA[pos]).to_bytes(4, byteorder='big')
            else:
                print('el valor no és ni 1 ni 2')
            pos += 1

    def makeBytesOrder(self, nOrder):
        '''
        Funcion para ordenar las variables para mesbook (entrada estado variables
        :param nOrder:
        :return:
        '''
        self.dataB = b''
        pos = 0
        for no in nOrder:
            for v in self.variables:
                if no == v[0]:
                    if v[1] == 1:
                        self.dataB += (self.dataA[pos]).to_bytes(2, byteorder='big')
                    elif v[1] == 2:
                        self.dataB += (self.dataA[pos]).to_bytes(4, byteorder='big')
            pos += 1

    def get_A(self):
        return self.dataA

    def get_B(self):
        return self.dataB

    def upgradeA(self,ar):
        self.dataA = ar

    def __str__(self):
        return str(self.data) + '\n' + str(self.dataA) + '\n' + str(self.dataB)



            #LECTURA JSON



#####################          LECTURA FITXER JSON              #######################
file = open("/home/root/config.json")
dicc_json = json.load(file)
file.close()

            #CONFIGURACIÓ JSON


        # LLISTA PER AVALUAR ELS TIPUS D'INTERRUPCIÓ
flanc = {'rising' : mraa.EDGE_RISING,'falling' : mraa.EDGE_FALLING,'both' : mraa.EDGE_BOTH}
        # LLISTA PER LA CONFIGURACIÓ DI10
dInput10 = {'di0' : 4,'di1' : 5,'di2' : 6,'di3' : 7,'di4' : 8,'di5' : 9,'di6' : 10,'di7' : 11,'di8' : 12,'di9' : 13,'di10' : 14}
        # LLISTA PER LA CONFIGURACIÓ DI5
dInput5 = {'di0' : 12,'di1' : 11,'di2' : 10,'di3' : 9,'di4' : 4}

        #VARIABLE PER GUARDAR LA CONFIGURACIÓ DI
conf_targ = None

        #DICCIONARI PLANTILLA
# dicc_conf = {'pIn': [0, 0], 'pOut': [0, 0], 'state': [0, 0], 'a0': [0, 0], 'a1': [0, 0], 'a2': [0, 0], 'a3': [0, 0], 'a4': [0, 0], 'a5': [0, 0], 'a6': [0, 0], 'a7': [0, 0]}


###########################          PROCESSAMENT JSON             ###########################
        #FUNCIONS ISR

def F_pin(a):           #SUMAR PEÇA ENTRADA
    di10.dataD['pIn'] += 1
    print('suma peça_in')

def F_pout(a):          #SUMAR PEÇA SORTIDA
    di10.dataD['pOut'] +=1
    print('suma peca-out')

def F_state(a):         #ESTAT MÀQUINA
    estat = obj_mraa['state'].read()
    if estat :
        di10.dataD['state'] = 1
    else :
        di10.dataD['state'] = 0
    print('state_scan')

def F_a0(a):            # ESTAT ALARMA 0 o scrap In
    print(dicc_json['variables']['scrapIn']['use'] == 'True')
    if 'scrapIn' in dicc_json['variables']:
        if dicc_json['variables']['scrapIn']['use'] == 'True':
            di10.dataD['scrapIn'] += 1
    else:
        a0 = obj_mraa['a0'].read()
        if a0:
            di10.dataD['a0'] = 1
        else:
            di10.dataD['a0'] = 0
        print('state_a0')

def F_a1(a):            # ESTAT ALARMA 1
    if 'scrapOut' in dicc_json['variables']:
        if dicc_json['variables']['scrapOut']['use'] == 'True':
            di10.dataD['scrapOut'] += 1
    else:
        a1 = obj_mraa['a1'].read()
        if a1:
            di10.dataD['a1'] = 1
        else:
            di10.dataD['a1'] = 0
        print('state_a1')

def F_a2(a):            # ESTAT ALARMA 2
    estat = obj_mraa['a2'].read()
    if estat:
        di10.dataD['a2'] = 1
    else:
        di10.dataD['a2'] = 0
    print('state_a2')
def F_a3(a):            # ESTAT ALARMA 3
    estat = obj_mraa['a3'].read()
    if estat:
        di10.dataD['a3'] = 1
    else:
        di10.dataD['a3'] = 0
    print('state_a3')
def F_a4(a):            # ESTAT ALARMA 4
    estat = obj_mraa['a4'].read()
    if estat:
        di10.dataD['a4'] = 1
    else:
        di10.dataD['a4'] = 0
    print('state_a4')
def F_a5(a):            # ESTAT ALARMA 5
    estat = obj_mraa['a5'].read()
    if estat:
        di10.dataD['a5'] = 1
    else:
        di10.dataD['a5'] = 0
    print('state_a5')
def F_a6(a):            # ESTAT ALARMA 6
    estat = obj_mraa['a6'].read()
    if estat:
        di10.dataD['a6'] = 1
    else:
        di10.dataD['a6'] = 0
    print('state_a6')


# CONFIGURACIÓ DI
# if dicc_json['protocol'] == 'gpio'
if dicc_json['targeta'] == 'DI10':conf_targ = dInput10
else: conf_targ = dInput5

if 'scrapIn' in dicc_json['variables'] and 'a0' in dicc_json['variables']:
    if dicc_json['variables']['scrapIn']['use'] == 'True' and  dicc_json['variables']['a0']['use'] == 'True':
        print("ERROOOR, no es pot posar scrapIn i a0")
        exit()
if 'scrapOut' in dicc_json['variables'] and 'a1' in dicc_json['variables']:
    if dicc_json['variables']['scrapOut']['use'] == 'True' and dicc_json['variables']['a1']['use'] == 'True':
        print("ERROOOR, no es pot posar scrapIn i a0")
        exit()
obj_mraa = {}
print(len(dicc_json['variables']))
# CARREGUEM EL FITXER JSON A LA PLANTILLA
for value in dicc_json['variables']:
    if dicc_json['variables'][value]['use']=='True':
        print(value)
        obj_mraa[value] = mraa.Gpio(conf_targ[dicc_json['variables'][value]['port']])  # CONF PORT DEL PIN
        obj_mraa[value].dir(mraa.DIR_IN)  # CONF PORT COM A ENTRADA
        # INICIALITZACIÓ I CONFIGURACIONS GPIO+ISR
        if value == 'pIn':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_pin, obj_mraa[value])    #INICIALITZEM INTERRUPCIÓ AL PIN CONFIGURAT COM A ENTRADA
        elif value == 'pOut':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_pout, obj_mraa[value])
        elif value == 'state':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_state, obj_mraa[value])
        elif value == 'scrapIn':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a0, obj_mraa[value])
        elif value == 'scrapOut':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a1, obj_mraa[value])
        elif value == 'a0':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a0, obj_mraa[value])
        elif value == 'a1':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a1, obj_mraa[value])
        elif value == 'a2':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a2, obj_mraa[value])
        elif value == 'a3':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a3, obj_mraa[value])
        elif value == 'a4':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a4, obj_mraa[value])
        elif value == 'a5':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a5, obj_mraa[value])
        elif value == 'a6':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a6, obj_mraa[value])
        elif value == 'a7':
            obj_mraa[value].isr(flanc[dicc_json['variables'][value]['interrupt']], F_a7, obj_mraa[value])
        else:
            print('senyal no definida')

print(obj_mraa)

class DI10():
                            #INICIALITZACIÓ VARIABLES GLOBALS MÀQUINA
    dataD = {"pIn":0, "pOut":0, "state":0,
            "a0":0, "a1":0, "a2": 0,
            "a3" : 0, "a4":0, "a5":0,
            "a6" : 0, "scrapIn": 0, "scrapOut" :0}
    # pIn = 0; pOut = 0; state = 0
    # a0 = 0; a1 = 0; a2 = 0
    # a3 = 0; a4 = 0; a5 = 0
    # a6 = 0; scrapIn = 0; scrapOut =0

    def __init__(self):
        self.data_info = []
        self.dataA = []
                            #LECTURA INICIAL VARIABLES MÀQUINA
        for a in obj_mraa:
            if a == 'state':
                self.dataD['state'] = obj_mraa[a].read()
            elif a =='a0':
                self.dataD["a0"] = obj_mraa[a].read()
            elif a =='a1':
                self.dataD["a1"] = obj_mraa[a].read()
            elif a =='a2':
                self.dataD["a2"] = obj_mraa[a].read()
            elif a =='a3':
                self.dataD["a3"] = obj_mraa[a].read()
            elif a =='a4':
                self.dataD["a4"] = obj_mraa[a].read()
            elif a =='a5':
                self.dataD["a5"] = obj_mraa[a].read()
            elif a =='a6':
                self.dataD["a6"] = obj_mraa[a].read()



    def readData(self):     #LECTURA ESTAT VARIABLES MÀQUINA
        self.dataA = []
        for k in self.dataD:
            if k in dicc_json['variables']:
                if dicc_json['variables'][k]['use'] == 'True':
                    self.dataA.append(self.dataD[k])
            elif k == 'pOut':
                self.dataA.append(self.dataD['pIn'])
        return True



#Creació de l'objecte di10

di10 = DI10()
