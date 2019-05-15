# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:38:01 2019

@author: Publico


"""
"""
esto es lo mismo de antes , probando solo como funciona le hecho de solo agregar el 
MesageBasedManager, para ahorrarnos de escribir las lineas que encuentran el instrumento

"""
from lantz import MessageBasedDriver
#from lantz.core import mfeats


# Definimos una clase osciloscopio con algunos metodos y que herede os de MBD
class Osciloscopio(MessageBasedDriver): 
    
    def idn(self):
        return self.query('*IDN?')
    
    def get_timebase(self):
        return float(self.query('HOR:MAIN:SCA?'))
    
    def set_timebase(self, value):
        return self.write('HOR:MAIN:SCA {}' . format(value))
    

'''
Esto inicializa el instrumento, opera y lo cierra. Lo que quede fuera no se corre
'''
with Osciloscopio.via_usb('C065093') as osci:

    print(osci.idn())
    osci.set_timebase(0.01)   # setea el timebase
    print(osci.get_timebase()) # devuelve el valor del timebase



#%%
"""
Lo que hacemos aca es probar como se utilizan los decoradores
"""


from lantz import MessageBasedDriver, Feat
#from lantz.core import mfeats


# Definimos una clase osciloscopio con algunos metodos y que herede os de MBD
class Osciloscopio(MessageBasedDriver): 
    
    def idn(self):
        return self.query('*IDN?')
    
    @Feat()  # Decorador que modifica la forma de usar el get y set
    def timebase(self):  # aca defino lo que va a hacer el get
        return float(self.query('HOR:MAIN:SCA?'))
    
    @timebase.setter  # el nombre previo a .setter tiene que ser el mismo que defino arriba
    def timebase(self, value):  # defino lo que hace el set
        return self.write('HOR:MAIN:SCA {}' . format(value))
    

with Osciloscopio.via_usb('C065093') as osci:

    print(osci.idn())
    print(osci.timebase)  # hace el get timebase
    osci.timebase = 0.01  # setea el timebase
    print(osci.timebase)

#%%
     

from lantz import MessageBasedDriver
#from lantz.core import mfeats


# Definimos una clase osciloscopio con algunos metodos y que herede os de MBD
class GeneradorFunciones(MessageBasedDriver): 
    
    def idn(self):
        return self.query('*IDN?')
    
    def GetVoltage(self, channel = 1):
        return self.query('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?'.format(channel))
    
    def SetVoltage(self, voltage, channel = 1): #gen.SetVoltage(2) Vpp
        self.write('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}'.format(channel, voltage))

with GeneradorFunciones.via_usb('C036493') as genfun:

    print(genfun.idn())
    print(genfun.GetVoltage)
    genfun.SetVoltage('1')


#%%
    
from lantz import MessageBasedDriver, Feat
from lantz.log import log_to_screen, DEBUG
#from lantz.core import mfeats


# Definimos una clase osciloscopio con algunos metodos y que herede os de MBD
class GeneradorFunciones(MessageBasedDriver): 
    
    def idn(self):
        return self.query('*IDN?')
    
    @Feat()
    def voltage(self, channel = 1):
        return float(self.query('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?'.format(channel)))
    
    @voltage.setter
    def voltage(self, voltage, channel = 1): #gen.SetVoltage(2) Vpp
        self.write('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}'.format(channel, voltage))

with GeneradorFunciones.via_usb('C033250') as genfun:

#    print(genfun.idn())
#    print(genfun.voltage)
#    genfun.voltage = 0.01
#    print(genfun.voltage)
    genfun.freq

    

#log_to_screen(DEBUG)
    