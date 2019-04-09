# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 17:07:31 2019

@author: Publico
"""

import visa

#armamos una funcion que averigue el numero de serie para el usuario
# Luego que el ususario meta ese numero de serie como input para lo demas

#def instrumento():
#    
#    rm = visa.ResourceManager()    # Devuelve todos los recursos conectados 
#    a=rm.list_resources()    # arma una tupla con los instrumentos 
#    
##    if equipo[0:21]=='USB0::0x0699::0x0346:':
#    for i in range( 0 , len(a)):    # Selecciona todos
#        inst = rm.open_resource(a[i])  # Abre el instrumento
##        out[i]=inst[i].query("*IDN?")
#        salida=inst.query("*IDN?")
#    return salida


#%%    
import visa

class GeneradorFunciones: 

    def __init__(self,serialno):
        rm = visa.ResourceManager()    # Devuelve todos los recursos conectados 
        self.serialno=serialno
        self.inst = rm.open_resource('{}'.format(serialno))
        
    def idn(self):
        self.inst.query("*IDN?")
        
    def frecuencia(self,HZ):
        self.inst.write(':SOURCE:FREQUENCY {}HZ'.format(HZ))  # Cambia la frecuencia del generador    

    def amplitud(self):
#        self.inst.write('SOUR1:VOLT:LEVel:IMMediate:AMPLitude{}'.format(percent))
        return self.inst.query('SOURce:VOLTage:LEVel:IMMediate:AMPLitude')



# Hace el usuario        
x = GeneradorFunciones('USB0::0x0699::0x0346::C033248::INSTR')
c  = x.idn()
#print(x.amplitud())
        