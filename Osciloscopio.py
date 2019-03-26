# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:21:49 2019

@author: Publico
"""

#%%
#Esta primera parte habilita el generador de funciones para comandos por pc
#para cualquier osciloscopio 
#
import visa 
rm = visa.ResourceManager()    # Devuelve todos los recursos conectados 
a = rm.list_resources()    # arma una tupla con los instrumentos 
print(a)
#osc = rm.open_resource('USB0::0x0699::0x0363::C065087::INSTR')
#print(osc.query('*IDN?'))   # Devuelve el nombre del instrumento. Hace un write seguido por un read
#osc.read_ascii_values('CURV?')
#%% Seleccionamos el instrumento 

#for i in range( 0 , len(a)):    # Selecciona un Osciloscopio
#    if a[i][0:21]=='USB0::0x0699::0x0363:': # Seleccionamos elemento i desde caracter 0 al 20  y 'Conexion :: Fabricante :: Modelo :: Numero de serie'
#        inst = a[i]
#    break
osc = rm.open_resource(a[0])  # Abre el instrumento
print(osc.query('*IDN?'))   # Devuelve el nombre del instrumento. Hace un write seguido por un read

## Ahora el instrumento es un objeto de Python

#print(type(osc))

# Frente a un error de read probar primero apagar la pc
# Vamos a tener dos comandos basicos help(inst.read) y help(inst.write)
# inst.write('*IDN?' , '\n') # hace el query y luego de la coma le pedi la terminacion
# inst.read()
# estas dos lineas de comando reemplazan el inst.query() de manera mas larga

#%%

#osc.query('WFMP:XUN')
#osc.read()
#DATa:SOUrce
osc.write('CURV?')
osc.read_raw()
#osc.query('TST')

