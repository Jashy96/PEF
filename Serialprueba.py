# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 13:00:53 2018

@author: ADMIN
"""
import serial
import time
import numpy as np
BAUDRATE= 9600
SerialportPIC1="COM6"

#SerialportPIC2="COM3"
    #Iniciar puerto Serial con la creación de un objeto de la clase Serial:
PIC1=serial.Serial(SerialportPIC1, BAUDRATE)
PIC1.close()
PIC1.open()
sensores=[]
while True:
    print("Inicio:\n")
    a=input("HOLA")
    a=a.encode("utf-8")
    PIC1.write(a)
    Lectura=PIC1.readline()
    Lectura=Lectura.decode("utf-8")
    Lectura=Lectura[0:len(Lectura)-3]
    Lectura=Lectura.replace(" ","")
    Lectura=Lectura.split(",")
    Datos=[int(i) for i in Lectura]
    print(Datos)
    print(np.sum(Datos))
    time.sleep(.05)