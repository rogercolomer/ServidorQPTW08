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
            if self.variables[v]['use']:
                if self.variables[v]['len'] == 1:
                    l += 1
                elif self.variables[v]['len'] == 2:
                    l += 2
                else:
                    print('Ops ! No es pot agafar la longitud de la dada '+v+' correctament')
        print(l)
        return l

    def makeArray(self):
        pos = 0
        self.dataA = []
        for var in self.variables:
            if self.variables[var]['use'] == 'True':  # ha destar plena
                if self.variables[var]['len'] == 1:  # 2 bytes
                    self.dataA.append(self.data[pos])
                    pos += 1
                elif self.variables[var]['len'] == 2:  # 4 bytes
                    self.dataA.append(UintDuint(self.data[pos], self.data[pos + 1]))
                    pos += 2
                else:
                    print('el valor no és ni 1 ni 2')
            else:
                self.dataA.append(0)

    def get_A(self):
        return self.dataA

    def get_B(self):
        return self.dataB

    def upgradeA(self,ar):
        self.dataA = ar

    def __str__(self):
        return str(self.data) + '\n' + str(self.dataA) + '\n' + str(self.dataB)


class UART(Comunication):
    def __init__(self, v, port):  # ordre variables, longitud lectura
        import serial
        super().__init__(v)
        # IOT2040 port = ttyS2
        # IOT2050A port = ttyUSB0
        self.ser = serial.Serial(port=port,
                                 baudrate=9600,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.SEVENBITS,
                                 timeout=1)

        #Modificaio llongitud directament de la classe pare
        # for v in self.variables:
        #     if v[2]==1:
        #         count += 1
        #     elif v[2] == 2:
        #         count += 2

        self.rang = self.len0

    def readData(self):
        # try:
        self.data = []
        a = str(self.ser.readline())  # La lectura de la UART la passem a string
        print(a)
        if a:
            for j in range(2, self.rang*4,4):
                b = ''
                for k in range(4):
                    b = b + a[j + k]
                self.data.append(int('0x' + b, 16))
        self.upgradeA(self.data)
        return True
        # except:
        #     return False


class Modbus(Comunication):
    def __init__(self, v, host):  # ordre variables, longitud lectura
        from pymodbus.client.sync import ModbusTcpClient
        super().__init__(v)
        self.host = host  # 192.168.250.1
        self.client = ModbusTcpClient(self.host, 502)

    def readData(self):
        self.client.connect()
        try:
            rr = self.client.read_holding_registers(0x000, self.len0 + 3, unit=0)  #adressa, numero , nideia123
            self.data = rr.registers
            if 'scrapIn' in self.variables and 'scrapOut' in self.variables:
                if self.variables['scrapIn']['use'] == "True" and self.variables['scrapOut']['use'] == "True":
                    self.data.pop(9)
                elif self.variables['scrapIn']['use'] == "True" and self.variables['scrapOut']['use'] == "False":
                    for i in [7,7,7]:self.data.pop(i)
                elif self.variables['scrapIn']['use'] == "False" and self.variables['scrapOut']['use'] == "True":
                    for i in [5,5,7]:self.data.pop(i)
                else:
                    for i in [5,5,5,5,5]:self.data.pop(i)
            elif 'scrapIn' in self.variables:
                if self.variables['scrapIn']['use'] == 'True':
                    for i in [7,7,7]:self.data.pop(i)
                else:
                    for i in [5, 5, 5, 5, 5]: self.data.pop(i)
            elif 'scrapOut' in self.variables:
                if self.variables['scrapIn']['use'] == 'True':
                    for i in [5, 5, 7]: self.data.pop(i)
                else:
                    for i in [5, 5, 5, 5, 5]: self.data.pop(i)
            else:
                for i in [5, 5, 5, 5, 5]: self.data.pop(i)

            self.client.close()
            time.sleep(0.5)
        except:
            self.client.close(),
            print('fail to connect Modbus')
        if self.data:
            self.makeArray()
            print(self.dataA)
            return True
        else:
            print('Theres no data')
            return False

class ModbusRTU(Comunication):
    def __init__(self, v,port):
        super().__init__(v)
        from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        os.system("switchserialmode /dev/ttyS2 rs485 --terminate")
        self.client = ModbusClient(method='rtu',
                                   port=port,
                                   stopbits=1,
                                   parity='E',
                                   baudrate=38400,
                                   timeout=0.1,
                                   unit=1
                                   )

    def readData(self):
        self.client.connect()
        try:
            state = self.client.read_holding_registers(address=500, count=1, unit=0x01)
            pIn = self.client.read_holding_registers(address=508, count=2, unit=0x01)
            alarm = self.client.read_holding_registers(address=540, count=2, unit=0x01)
            self.data = [pIn.registers[0], pIn.registers[1], state.registers[0], alarm.registers[0], alarm.registers[0]]
            self.client.close()
        except Exception as e:
            self.client.close()
            print('fail to connect Modbus '+str(e))
        if self.data:
            self.makeArray()
            if self.dataA[2] == 1:
                self.dataA[2] = 2
            elif self.dataA[2] == 2:
                self.dataA[2] = 1
            elif self.dataA[2] == 3:
                self.dataA[2] = 0
            return True
        else:
            print('Theres no data')
            return False


class S7(Comunication):

    def __init__(self, v, host, db):  # ordre variables, longitud lectura
        super().__init__(v)
        # TODO delete port
        self.host = host  # 192.168.250.1
        self.db = db
        self.len0 = self.len0*2
        self.plc = c.Client()


    def readData(self):
        try:

            self.plc.connect(self.host, 0, 1)  # ip
            connection = 1
        except:
            connection = 0
            self.plc.disconnect()
        if connection == 1:
            try:
                self.data = []
                value = self.plc.db_read(self.db, 0, self.len0)  # llegir db (numero_db,primer byte, longitud maxima)
                # agrupem per les variables per bytes
                compt = 0
                for v in self.variables:
                    if v[2] == 1:
                        if v[1] == 1:
                            self.data.append(
                                int.from_bytes([value[compt], value[compt + 1]], byteorder='big', signed=False))
                            compt += 2
                        elif v[1] == 2:
                            self.data.append(
                                int.from_bytes([value[compt], value[compt + 1], value[compt + 2], value[compt + 3]],
                                               byteorder='big', signed=False))
                            compt += 4
                self.plc.disconnect()
                self.makeArray()
                return True
            except:
                return False
        else:
            return False

    def makeArray(self):
        '''Com que les variables ja estan concatenades no sha de fer amb el make array'''
        pos = 0
        self.dataA = []
        for var in self.variables:
            if var[2] == 1:  # ha destar plena
                self.dataA.append(self.data[pos])
                pos += 1
            elif var[2] == 0:
                self.dataA.append(0)


class USB(Comunication):
    def __init__(self, v):  # ordre variables, longitud lectura
        super().__init__(v)
        # import usb.core
        # import usb.util
        # import sys
        # import time
        # import struct

        IDVENDOR = 1424
        IDPRODUCT = 91
        core_con = 0
        while (core_con == 0):
            try:
                self.dev = usb.core.find(idVendor=IDVENDOR, idProduct=IDPRODUCT)
                core_con = 1
                if self.dev is None:
                    raise ValueError('Device not found')
            except:
                core_con = 0

        self.endpoint_in = self.dev[0][(0, 0)][0]
        self.endpoint_out = self.dev[0][(0, 0)][1]
        self.RunPlc()

    def USBwrite(self, msg, revlen):
        x = 0
        cnt1 = 0
        cnt2 = 0
        data = []
        while (1):
            try:
                if x == 0:
                    self.endpoint_out.write(msg)
                    x = 1

                data += self.dev.read(self.endpoint_in.bEndpointAddress, self.endpoint_in.wMaxPacketSize, timeout=20)
                if len(data) == revlen:
                    return data

            except usb.core.USBError as e:

                if e.strerror.find("error sending control message") >= 0:
                    cnt1 += 1
                    if cnt1 > 2:
                        raise ValueError('Over error sending control message')
                    x = 0
                    continue

                elif e.strerror.find("Connection timed out") >= 0:
                    cnt2 += 1
                    if cnt2 > 2:
                        raise ValueError('Over Connection timed out')
                    continue

                else:
                    raise ValueError(e.strerror)

    def PLC_Run_Monitoring(self):
        write_array = [0xAB, 0x00, 0x11, 0x80, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        write_array.append(randint(1, 0xFF))
        write_array += [0x04, 0x01, 0xFF, 0xFF, 0x02]
        sumcheck = sum(write_array)
        sumHi = ((sumcheck >> 8) & 0xFF)
        sumLo = (sumcheck & 0xFF)
        write_array.append(sumHi)
        write_array.append(sumLo)
        res = self.USBwrite(write_array, 19)
        if len(res) == 19:
            sum1 = res[len(res) - 2] << 8 | res[len(res) - 1]
            res.pop()
            res.pop()
            sum2 = sum(res)
            if sum1 == sum2:
                revc = [171, 0, 16, 192, 0, 2, 0, 0, 251, 0, 0, 0, 4, 1, 0, 0]
                res.pop(12)
                if res == revc:
                    print("PLC is Run Monitoring")
                else:
                    print("PLC Run Monitoring Error")
            else:
                print("PLC Run Monitoring Error")
        else:
            print("PLC Run Monitoring Error")

    def D_Read(self, D_number):
        write_array = [0xAB, 0x00, 0x16, 0x80, 0x00, 0x2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        rdm = randint(1, 0xFF)
        write_array.append(rdm)
        write_array += [0x01, 0x04, 0x07, 0x00, 0x00, 0x00, 0x82]
        write_array.append(D_number >> 8);
        write_array.append(D_number & 0xFF);
        write_array += [0x00]
        sumcheck = sum(write_array)
        sumHi = ((sumcheck >> 8) & 0xFF)
        sumLo = (sumcheck & 0xFF)
        write_array.append(sumHi)
        write_array.append(sumLo)
        res = self.USBwrite(write_array, 24)
        if len(res) == 24:
            val1 = res.pop()
            val2 = res.pop()
            sum1 = val2 << 8 | val1
            sum2 = sum(res)
            if sum1 == sum2:
                rdm2 = res.pop(12)
                if rdm == rdm2:
                    val1 = res.pop()
                    val2 = res.pop()
                    value = val2 << 8 | val1
                    val1 = res.pop()
                    val2 = res.pop()
                    revc = [171, 0, 21, 192, 0, 2, 0, 0, 251, 0, 0, 0, 1, 4, 0, 0, 7]
                    if res == revc:
                        return (1, value)
                    else:
                        return (1, value)
                else:
                    return (1, value)
            else:
                return (1, value)
        else:
            return (1, value)

    def RunPlc(self):
        con = 0
        while con == 0:
            self.PLC_Run_Monitoring()
            con = 1

    def readData(self):
        # TODO filtrar de les variables a llegir
        self.data = []
        # lectura pIn, pOut, state
        for i in range(600, 605):
            self.data.append(self.D_Read(i)[1])
        # lectura alarmes
        for i in range(610, 616):
            self.data.append(self.D_Read(i)[1])
        self.makeArray()
        print(self.dataA)
        return True
        # # TODO filtrar de les variables a llegir
        # # try:
        # self.data = []
        # # lectura pIn, pOut, state
        # if self.variables[0][2] == 1 and self.variables[1][2] == 1:
        #     for i in range(600, 605):
        #         self.data.append(self.D_Read(i)[1])
        # elif self.variables[0][2] == 1 and self.variables[1][2] == 0:
        #     for i in range(600, 602):
        #         self.data.append(self.D_Read(i)[1])
        #     self.data.append(self.D_Read(604)[1])
        # # lectura alarmes
        # for i in range(610, 616):
        #     self.data.append(self.D_Read(i)[1])
        # self.makeArray()
        # self.makeBytes()
        # #     return True
        # # except:
        #     return False




''' Aquest modul servirà per els robots amb IOT2050 i 10 DI
    És un mòdul especial ja que l'objecte està definit aquí 
    el nom de la classe és DI10 com el nom de la variable de l'objecte
    És la una manera que s'ha aconseguit fer un mòdul especial.
    Autor : Roger Colomer
    Data: 05/02/2020
    v1.0
    '''

def pIn_isr(a):
    c.piezasProcessadas += 1
    print(c.piezasProcessadas)


def DI1_isr(a):
    print('5')
    c.estadoLinea = d1.read()
    c.save_data()


def DI2_isr(a):
    print('Taula A')
    if d2.read() == 1:
        c.marchaMaquina = 1
        # fallor robot
    else:
        c.marchaMaquina = 0
    c.save_data()


def DI3_isr(a):
    print('Taula B')
    if d3.read() == 1:
        c.marchaMaquina = 2
        # falta de producte
    else:
        c.marchaMaquina = 0
    c.save_data()


def DI4_isr(a):
    print('8')
    if d4.read() == 1:
        c.marchaMaquina = 3
        # falta de producte
    else:
        c.marchaMaquina = 0
    c.save_data()


D0 = mraa.Gpio(4)
D0.dir(mraa.DIR_IN)
D0.isr(mraa.EDGE_RISING, pIn_isr, D0)

d1 = mraa.Gpio(5)
d1.dir(mraa.DIR_IN)
d1.isr(mraa.EDGE_BOTH, DI1_isr, d1)

d2 = mraa.Gpio(6)
d2.dir(mraa.DIR_IN)
d2.isr(mraa.EDGE_RISING, DI2_isr, d2)

d3 = mraa.Gpio(7)
d3.dir(mraa.DIR_IN)
d3.isr(mraa.EDGE_RISING, DI3_isr, d3)

d4 = mraa.Gpio(8)
d4.dir(mraa.DIR_IN)
d4.isr(mraa.EDGE_BOTH, DI4_isr, d4)


def readD1():
    return d1.read()

class DI10():
    piezasProcessadas = 0
    estadoLinea = readD1()
    marchaMaquina = 0

    def __init__(self):
        self.dataA = []

    def readData(self):
        self.dataA = [self.piezasProcessadas, self.piezasProcessadas, self.estadoLinea]
        return True

    def resetData(self):
        self.piezasProcessadas = 0


di10 = DI10()
