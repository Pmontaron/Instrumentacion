# -*- coding: utf-8 -*-
"""
Created on Tue May 28 15:47:01 2019

@author: Publico
"""

#importo las librerias
import visa
import numpy as np
import matplotlib.pyplot as plt
import GenFunLantz 
import NIDAQ


#%%
#Primero vemos que elementos estan conectados y abrimos el generador de 
# funciones para hallar su numero de serie
rm = visa.ResourceManager()    # Devuelve todos los recursos conectados 
a=rm.list_resources()    # arma una tupla con los instrumentos 
print(a)

for i in range( 0 , len(a)):    # Selecciona un Tektronix
    if a[i][0:21]=='USB0::0x0699::0x0346:': # Seleccionamos elemento i desde caracter 0 al 20  y 'Conexion :: Fabricante :: Modelo :: Numero de serie'
        tektronix = a[i]
    break
inst = rm.open_resource(tektronix)  # Abre el instrumento
print(inst.query("*IDN?"))   # Devuelve el nombre del instrumento. Hace un write seguido por un read

## Ahora el instrumento es un objeto de Python

serialno =inst.query("*IDN?")[19:26]

#%%

# La variable port debe ser una lista
port = [1,2]
A = 1   # valor de amplitud a utilizar en V
frec = 1

with GenFunLantz.GeneradorFunciones.via_usb(serialno) as genfun:
    genfun.voltage = A # Amplitud constante 
    genfun.frequency = frec
    genfun.shape = 'ramp'

# Corremos la cantidad de muestras por segundo en DIFF para los dos puertos en simultaneo
#with NIDAQ.NIDAQ(port) as nidaq:
NIDAQ.NIDAQ.set_sample_rate_continuous(sample_rate=10000)

nidaq = NIDAQ.NIDAQ(port)
datos_diff = nidaq.getvoltage_ai_DIFF(10000)

##%%
#plt.plot(datos_diff[0],'.')    
#plt.plot(datos_diff[1],'.')
##print(len(datos_diff[0]))
