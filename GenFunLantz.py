# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 15:34:20 2019

@author: Publico
"""

from lantz import MessageBasedDriver, Feat
#from lantz.core import mfeats

class GeneradorFunciones(MessageBasedDriver):
    
    def idn(self):
        return self.query('*IDN?')    
    
    
#    Revisar esto y corregirlo
#    @Feat() #esto deberia encender o apagar el canal utilizando ON u OFF, por defecto es el canal 1
#    def power(self, channel = 1):
#        self.write("OUTPut{}:STATe?".format(channel))
#    
#    @power.setter
#    def power(self, STAT, channel = 1): #frequency ='5 kHz' o por default en Hz te setea la frequencia
#        self.write("OUTPut{}:STATe{}".format(channel,STAT))
   
    
    @Feat()
    def frequency(self, channel = 1): #frequency('numero') te devuelve la frequencia del canal 'numero'
        return float(self.query('SOURce{}:FREQuency?'.format(channel)))
    
    @frequency.setter
    def frequency(self, freq, channel = 1): #frequency ='5 kHz' o por default en Hz te setea la frequencia
        self.write("SOURce{}:FREQuency {}".format(channel,freq))
    
    @Feat() # devuelve el nombre de la forma
    def shape(self, channel = 1):
        return self.query('SOURce{}:FUNCtion:SHAPe?'.format(channel))
    
    @shape.setter
    def shape(self, shape, channel = 1): #gen.SetShape('SQUare')
        self.write("SOURce{}:FUNCtion {}".format(channel,shape)) 
    
    @Feat()
    def voltage(self, channel = 1):
        return float(self.query('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?'.format(channel)))
    
    @voltage.setter
    def voltage(self, voltage, channel = 1): #gen.SetVoltage(2) Vpp
        self.write('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}'.format(channel, voltage))
        
#    def GetOffset(self, channel = 1):
#        return self.inst.query('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet?'.format(channel))        
#    
#    def SetOffset(self, offset, channel = 1): #gen.SetOffset(1) V
#        self.inst.write('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet {}'.format(channel, offset))    
#        
#%%        
        
with GeneradorFunciones.via_usb('C036493') as genfun:

    print(genfun.idn())
    print(genfun.voltage)
    genfun.voltage = 0.1
#    print(genfun.power)
    genfun.frequency = 1000
    #genfun.shape = ''
    print(genfun.voltage)


