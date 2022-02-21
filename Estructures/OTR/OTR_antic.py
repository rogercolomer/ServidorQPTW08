#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  OTR_v3.py
#
import mysql.connector
import time
import serial
import ast
import json
import telebot
import numpy as np
import RPi.GPIO as GPIO
from datetime import datetime

time.sleep(0)
alarm_name = ['', 'NO OK SETA DE EMERGENCIA',
              'NO OK ALIMENTACIÓN RELÉ SEGURIDAD',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'RESERVA TIPO 1',
              'NO CONFIRMACIÓN OK VARIADOR VENTILADOR V101 (E17.1) (TIPO 2)',
              'NO OK PROTECCIÓN VARIADOR VENTILADOR V101 (E17.0) (TIPO 2)',
              'NO OK PROTECCIÓN VENTILADOR QUEMADOR DX-101 (E0.5) (TIPO 2)',
              'NO OK PROTECCIÓN MANIOBRA QUEMADOR DX-101 (E0.7) (TIPO 2)',
              'NO OK PROTECCIÓN GENERAL (E0.2) (TIPO 2)',
              'ALARMA INCREMENTO/ALTA TEMPERATURA TORRE 1 (TIPO2)',
              'ALARMA INCREMENTO/ALTA TEMPERATURA TORRE 2 (TIPO2)',
              'ALARMA INCREMENTO/ALTA TEMPERATURA TORRE 3 (TIPO2)',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'RESERVA TIPO 2',
              'FALLO VÁLVULA ENTRADA GASES TORRE 1 V111',
              'FALLO VÁLVULA SALIDA GASES TORRE 1 V121',
              'FALLO VÁLVULA PURGA TORRE 1 V131',
              'FALLO VÁLVULA ENTRADA GASES TORRE 2 V112',
              'FALLO VÁLVULA SALIDA GASES TORRE 2 V122',
              'FALLO VÁLVULA PURGA TORRE 2 V132',
              'FALLO VÁLVULA ENTRADA GASES TORRE 3 V113',
              'FALLO VÁLVULA SALIDA GASES TORRE 3 V123',
              'FALLO VÁLVULA PURGA TORRE 3 V133',
              'FALLO VÁLVULA ENTRADA GASES PRINCIPAL V001',
              'FALLO VÁLVULA ENTRADA AIRE AMBIENTE V002',
              'NO OK PROTECCIÓN VÁLVULAS RTO (E0.2) (TIPO 3)',
              'RESERVA TIPO 3',
              'RESERVA TIPO 3',
              'RESERVA TIPO 3',
              'RESERVA TIPO 3',
              'FALLO LLAMA QUEMADOR DX101 (E1.2) (TIPO 4)',
              'NO OK QUEMADOR EN SERVICIO DX101 EN ETAPAS 4 5 6 (E1.1) (TIPO 4)',
              'NO OK PRESOSTATO MÍNIMA GAS QUEMADOR DX101 (TIPO 4)',
              'NO OK PRESOSTATO MÁXIMA GAS QUEMADOR DX101 (TIPO 4)',
              'NO OK PRESOSTATO MÍNIMA AIRE QUEMADOR DX101 (TIPO 4)',
              'NO OK F.C. POSICIONADOR CERRADO QUEMADOR DX101 EN ETAPAS 7 8 9 (E17.4) (TIPO 4)',
              'FALLO TEST HERMETICIDAD QUEMADOR DX101 (E17.3) (TIPO 4)',
              'NO OK PROTECCIÓN VÁLVULAS FOCOS (E0.4) (TIPO 4)',
              'NO OK TERMOSTATO QUEMADOR DX101 (E17.2) (TIPO 4)',
              'RESERVA TIPO 4',
              'RESERVA TIPO 4',
              'RESERVA TIPO 4',
              'RESERVA TIPO 4',
              'RESERVA TIPO 4',
              'RESERVA TIPO 4',
              'RESERVA TIPO 4',
              'ROTURA DE HILO TRANSMISOR DE PRESIÓN CIRCUITO ASPIRACIÓN PT102 (PEW140) (TIPO 5)',
              'ROTURA DE HILO SONDA TEMPERATURA CÁMARA TE107 (PEW 132) (TIPO 5)',
              'AHH TEMPERATURA CÁMARA TE107',
              'AHH TRANSMISOR DE PRESIÓN PT102',
              'ROTURA DE HILO SONDA TEMPERATURA PURGA GASES TE106 (PEW134) (TIPO 5)',
              'AHH TEMPERATURA PURGA TE108',
              'ROTURA DE HILO SONDA TOLVA TORRE 1 TE111 (PEW208) (TIPO 5)',
              'ROTURA DE HILO SONDA TOLVA TORRE 1 TE112 (PEW210) (TIPO 5)',
              'ROTURA DE HILO SONDA TOLVA TORRE 1 TE113 (PEW212) (TIPO 5)',
              'RESERVA TIPO 5',
              'RESERVA TIPO 5',
              'RESERVA TIPO 5',
              'RESERVA TIPO 5',
              'RESERVA TIPO 5',
              'RESERVA TIPO 5',
              'RESERVA TIPO 5',
              'ROTURA DE HILO TRANSMISOR DE PRESIÓN ENTRADA GASES TORRES PT103 (PEW136) (TIPO 6)',
              'ROTURA DE HILO TRANSMISOR DE PRESIÓN SALIDA GASES TORRES PT104 (PEW 138) (TIPO 5)',
              'ROTURA DE HILO SONDA TEMPERATURA ENTRADA GASES TE101 (PEW128) (TIPO 6)',
              'ROTURA DE HILO SONDA TEMPERATURA SALIDA GASES TE105 (PEW130) (TIPO 6)',
              'AHH PÉRDIDA DE CARGA RTO (PT104 - PT103) (TIPO 6)',
              'RESERVA TIPO 6',
              'ROTURA DE HILO TRANSMISOR PT109 (PEW 142) (TIPO 6)',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'RESERVA TIPO 6',
              'NO OK PERMISO DEPURACIÓN LINEA ESTUFA (E19.0) (TIPO 7)',
              'FALLO VÁLVULA ENTRADA GASES COLECTOR KALFRISA LINEA ESTUFA FV409 (TIPO 7)',
              'FALLO VÁLVULA EMERGENCIA LINEA ESTUFA FV410 (TIPO 7)',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7',
              'RESERVA TIPO 7'
              'RESERVA TIPO 7',
              'NO OK PERMISO DEPURACIÓN LINEA 1 (E18.0) (TIPO 8)',
              'FALLO VÁLVULA ENTRADA GASES COLECTOR KALFRISA LINEA 1 FV401 (TIPO 8)',
              'FALLO VÁLVULA EMERGENCIA LINEA 1 FV402 (TIPO 8)',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'RESERVA TIPO 8',
              'NO OK PERMISO DEPURACIÓN LINEA 2 (E18.2) (TIPO 9)',
              'FALLO VÁLVULA ENTRADA GASES COLECTOR KALFRISA LINEA 2 FV403 (TIPO 9)',
              'FALLO VÁLVULA EMERGENCIA LINEA 2 FV404 (TIPO 9)',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'RESERVA TIPO 9',
              'NO OK PERMISO DEPURACIÓN LINEA 3 (E18.4) (TIPO 10)',
              'FALLO VÁLVULA ENTRADA GASES COLECTOR KALFRISA LINEA 3 FV405 (TIPO 10)',
              'FALLO VÁLVULA EMERGENCIA LINEA 2 FV406 (TIPO 10)',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'RESERVA TIPO 10',
              'NO OK PERMISO DEPURACIÓN LINEA 4 (E18.4) (TIPO 11)',
              'FALLO VÁLVULA ENTRADA GASES COLECTOR KALFRISA LINEA 4 FV407 (TIPO 11)',
              'FALLO VÁLVULA EMERGENCIA LINEA 4 FV408 (TIPO 11)',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'RESERVA TIPO 11',
              'AHH PÉRDIDA DE CARGA FILTRO PT109 (TIPO 6)',
              'ALARMA FILTRO TECHNOTRAF',
              'AVISO FILTRO TECHNOTRAF',
              'RESERVA TIPO 12',
              'RESERVA SIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12',
              'RESERVA TIPO 12']
start = 0
while (start == 0):
    try:
        token = '867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs'
        tb = telebot.TeleBot(token)
        chat_roger = '743717839'
        chat_pep = '815134963'
        chat_joan = '409835547'
        enviat = 0
        estat_anterior = 6
        avis_alarma = 0
        enviar_alarma = 0

        ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS, timeout=1)
        start = 1
    except:
        print('error')
        start = 0
print('GAAAS')

while (True):
    data = ser.readline()
    if data:
        d = data.decode('utf-8')
        da = d.rstrip('\n')
        data_dic = ' '
        if d[0] == '{':
            data_dic = da
            print('paren')
            l = len(data_dic)
            if data_dic[l - 1] == '}':
                d = ast.literal_eval(data_dic)
                print(datetime.now())
                print(d)
                # append de tots els 16 bits de les 12 alarmes
                alarm_n = ['ATipo1', 'ATipo2', 'ATipo3', 'ATipo4', 'ATipo5', 'ATipo6', 'ATipo7',
                           'ATipo8', 'ATipo9', 'ATipo10', 'ATipo11', 'ATipo12']
                alarm_binary = []
                for an in alarm_n:
                    alarm_binary.append(format(d[an], "016b"))
                alarm_bit = []
                for i in range(12):
                    for j in range(15, -1, -1):
                        alarm_bit.append(alarm_binary[i][j])
                list_alarm = [1, 2, 17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 35, 36, 37, 38, 39, 40,
                              41, 42, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68,
                              69, 70, 71, 72, 73, 81, 82, 83, 84, 85, 86, 87, 97, 98, 99, 113, 114,
                              115, 129, 130, 131, 145, 146, 147, 161, 162, 163, 177, 178, 179]
                alarm_pos = []
                for k in list_alarm:
                    if alarm_bit[k] == '1':
                        alarm_pos.append(k)
                len_al = len(alarm_pos)

                # avisos alarmes (max6)
                if not alarm_pos:
                    alarma0 = 0
                    alarma1 = 0
                    alarma2 = 0
                    alarma3 = 0
                    alarma4 = 0
                    alarma5 = 0
                if alarm_pos:
                    if alarm_pos and len_al >= 6:
                        alarma0 = alarm_pos[0] + 1
                        alarma1 = alarm_pos[1] + 1
                        alarma2 = alarm_pos[2] + 1
                        alarma3 = alarm_pos[3] + 1
                        alarma4 = alarm_pos[4] + 1
                        alarma5 = alarm_pos[5] + 1
                        if enviar_alarma == 0:
                            try:
                                tb.send_message(chat_roger, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_roger, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                                tb.send_message(chat_roger, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                                tb.send_message(chat_roger, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                                tb.send_message(chat_roger, text=str(alarm_name[alarma4]), parse_mode="Markdown")
                                tb.send_message(chat_roger, text=str(alarm_name[alarma5]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma4]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma5]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma4]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma5]), parse_mode="Markdown")
                                enviar_alarma = 1
                            except:
                                print('caca')
                        else:
                            pass
                    elif alarm_pos and len_al == 5:
                        alarma0 = alarm_pos[0] + 1
                        alarma1 = alarm_pos[1] + 1
                        alarma2 = alarm_pos[2] + 1
                        alarma3 = alarm_pos[3] + 1
                        alarma4 = alarm_pos[4] + 1
                        alarma5 = 0
                        if enviar_alarma == 0:
                            tb.send_message(chat_roger, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma4]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma4]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma4]), parse_mode="Markdown")
                            enviar_alarma = 1
                        else:
                            pass
                    elif alarm_pos and len_al == 4:
                        alarma0 = alarm_pos[0] + 1
                        alarma1 = alarm_pos[1] + 1
                        alarma2 = alarm_pos[2] + 1
                        alarma3 = alarm_pos[3] + 1
                        alarma4 = 0
                        alarma5 = 0
                        if enviar_alarma == 0:
                            tb.send_message(chat_roger, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma3]), parse_mode="Markdown")
                            enviar_alarma = 1
                        else:
                            pass
                    elif alarm_pos and len_al == 3:
                        alarma0 = alarm_pos[0] + 1
                        alarma1 = alarm_pos[1] + 1
                        alarma2 = alarm_pos[2] + 1
                        alarma3 = 0
                        alarma4 = 0
                        alarma5 = 0
                        if enviar_alarma == 0:
                            tb.send_message(chat_roger, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_roger, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_joan, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                            tb.send_message(chat_pep, text=str(alarm_name[alarma2]), parse_mode="Markdown")
                            enviar_alarma = 1
                        else:
                            pass
                    elif alarm_pos and len_al == 2:
                        try:
                            alarma0 = alarm_pos[0] + 1
                            alarma1 = alarm_pos[1] + 1
                            alarma2 = 0
                            alarma3 = 0
                            alarma4 = 0
                            alarma5 = 0
                            if enviar_alarma == 0:
                                tb.send_message(chat_roger, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_roger, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma1]), parse_mode="Markdown")
                                enviar_alarma = 1
                            else:
                                pass
                        except:
                            print('endavant')
                    elif alarm_pos and len_al == 1:
                        try:
                            alarma0 = alarm_pos[0] + 1
                            alarma1 = 0
                            alarma2 = 0
                            alarma3 = 0
                            alarma4 = 0
                            alarma5 = 0
                            if enviar_alarma == 0:
                                tb.send_message(chat_roger, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_joan, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                tb.send_message(chat_pep, text=str(alarm_name[alarma0]), parse_mode="Markdown")
                                enviar_alarma = 1
                            else:
                                pass
                        except:
                            print('endavant')
                if alarm_pos:
                    if avis_alarma == 0:
                        m = '*OTR*:Hi ha una alarma activada (Estat:' + str(d['Estat_OTR']) + ')'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 1
                    else:
                        pass
                if d['Estat_OTR'] == 6:
                    if estat_anterior != 6:
                        m = '*OTR*: Torna a funcionar correctament'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 1:
                    if estat_anterior != 1:
                        m = '*OTR*: Hi ha la seguretat activada'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 2:
                    if estat_anterior != 2:
                        m = '*OTR*: La màquina està en mode repos'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 3:
                    if estat_anterior != 3:
                        m = "*OTR*: La màquina estè en mode purga"
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 4:
                    if estat_anterior != 4:
                        m = "*OTR*: La màquina està en mode escalfament"
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 5:
                    if estat_anterior != 5:
                        m = '*OTR*: La màquina està en mode commutació'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 7:
                    if estat_anterior != 7:
                        m = '*OTR*: La màquina està parada'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        alarma0 = 180
                        alarma1 = 180
                        alarma2 = 180
                        alarma3 = 180
                        alarma4 = 180
                        alarma5 = 180
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 8:
                    if estat_anterior != 8:
                        m = "*OTR*: La màquina s'està refredant"
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                elif d['Estat_OTR'] == 9:
                    if estat_anterior != 9:
                        m = '*OTR*: Hi han els variadors parats'
                        tb.send_message(chat_roger, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_joan, text=str(m), parse_mode="Markdown")
                        tb.send_message(chat_pep, text=str(m), parse_mode="Markdown")
                        avis_alarma = 0
                    else:
                        pass
                else:
                    pass
                estat_anterior = d['Estat_OTR']

                linies = format(d['Estat_linies'], "b")
                if len(linies) < 12:
                    space = 12 - (len(linies))
                    for i in range(space):
                        linies = "0" + linies
                l1 = linies[1]
                l2 = linies[4]
                l3 = linies[7]
                l4 = linies[10]
                print(l1, l2, l3, l4)
                lm = int(l1 + l2 + l3 + l4, 2)

                perdua_102_109 = d['PT102'] - d['PT109']
                perdua_103_104 = d['PT103'] - d['PT104']

                try:
                    mydb = mysql.connector.connect(
                        host='147.45.44.200',
                        user='ort2',
                        passwd='123456789',
                        database='OTR'
                    )
                    mycursor = mydb.cursor()
                    sql1 = """INSERT INTO otr(timestamp,Feedback_V101,Pot_cremador,Feedback_V002,TE101,TE105,TE107,TE108,TE111,TE112,TE113,PT102,PT103,PT104,PT109,PC103_104,PC102_109,Estat_OTR,"""
                    sql2 = """Estat_linies,Estat_filtres,V101,V102,V001,V011,V012,V013,V021,V022,V023,V031,V032,V033,V401,V402,V403,V404,V405,V406,V407,V408,ATipo1,ATipo2,ATipo3,ATipo4,ATipo5,ATipo6,ATipo7,ATipo8,ATipo9,ATipo10,ATipo11,ATipo12,lm,alarma0,alarma1,alarma2,alarma3,alarma4,alarma5,linia1,linia2,linia3,linia4)"""
                    sql3 = """ VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    val = [(datetime.now(), d['Feedback_V101'], d['Potencia_cremador'], d['Feedback_V002'], d['TE101'],
                            d['TE105'], d['TE107'], d['TE108'], d['TE111'], d['TE112'],
                            d['TE113'], d['PT102'], d['PT103'], d['PT104'], d['PT109'], perdua_103_104, perdua_102_109,
                            d['Estat_OTR'], d['Estat_linies'], d['Estat_filtres'], d['V101'], d['V102'], d['V001'],
                            d['V011'], d['V012'], d['V013'], d['V021'], d['V022'],
                            d['V023'], d['V031'], d['V032'], d['V033'], d['V401'], d['V402'], d['V403'], d['V404'],
                            d['V405'], d['V406'], d['V407'], d['V408'],
                            d['ATipo1'], d['ATipo2'], d['ATipo3'], d['ATipo4'], d['ATipo5'], d['ATipo6'], d['ATipo7'],
                            d['ATipo8'], d['ATipo9'], d['ATipo10'], d['ATipo11'], d['ATipo12'], lm, alarma0, alarma1,
                            alarma2, alarma3, alarma4, alarma5, l1, l2, l3, l4)]
                    mycursor.executemany(sql1 + sql2 + sql3, val)
                    mydb.commit()
                    mycursor.close()
                    print('')
                except:
                    print("error a l'escriure a la base de dades2")

                try:
                    except:
                    print("error a l'escriure a la base de dades rpi2")

