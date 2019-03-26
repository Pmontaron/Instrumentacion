# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:48:45 2019

@author: Publico
"""
#%%
#Esta primera parte habilita el generador de funciones para comandos por pc
#para cualquier textronix AFG3021B
#
import visa 
rm = visa.ResourceManager()    # Devuelve todos los recursos conectados
a=rm.list_resources()    # arma una tupla con los instrumentos
print(a)

for i in range( 0 , len(a)):    # Selecciona un Tektronix
    if a[i][0:21]=='USB0::0x0699::0x0346:': # Seleccionamos elemento i desde caracter 0 al 20
        instrumento = a[i]
    break
inst = rm.open_resource(instrumento)  # Abre el instrumento
print(inst.query("*IDN?"))   # Devuelve el nombre del instrumento

#%%
