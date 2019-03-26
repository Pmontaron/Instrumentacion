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
    if a[i][0:21]=='USB0::0x0699::0x0346:': # Seleccionamos elemento i desde caracter 0 al 20  y 'Conexion :: Fabricante :: Modelo :: Numero de serie'
        tektronix = a[i]
    break
inst = rm.open_resource(tektronix)  # Abre el instrumento
print(inst.query("*IDN?"))   # Devuelve el nombre del instrumento. Hace un write seguido por un read

## Ahora el instrumento es un objeto de Python
print(type(inst))

# Frente a un error de read probar primero apagar la pc
# Vamos a tener dos comandos basicos help(inst.read) y help(inst.write)
# inst.write('*IDN?' , '\n') # hace el query y luego de la coma le pedi la terminacion
# inst.read()
# estas dos lineas de comando reemplazan el inst.query() de manera mas larga


#%%
# Ahora tenemos que darle alguna orden al generador de funciones, primero levantar un valor y luego una tira de valores
inst.write(':SOURCE:FREQUENCY 10HZ')  # Cambia la frecuencia del generador




