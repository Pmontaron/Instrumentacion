# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:30:31 2019

@author: Publico
"""

import pyvisa
import time
import matplotlib as plt
import numpy as np


class GeneradorFunciones():
    
    def __init__(self,num_generador = 0):
        self.rm = pyvisa.ResourceManager()
        self.lista = self.rm.list_resources()
        self.generadores = []
        for i in range (0,len(self.lista)):
            if self.lista[i][6:21]=='0x0699::0x0346:': # Seleccionamos elemento i desde caracter 6 al 20  cuyo 'Fabricante :: Modelo::' coincidan
                self.generadores.append(self.lista[i])
               
                
                
        if self.generadores == []:
            print('No hay generadores conectados')
            
        self.inst = self.rm.open_resource(self.generadores[num_generador])  # Abre el primer instrumento de la lista
    
    
    def TurnOn(self, channel = 1):
        self.inst.write("OUTPut{}:STATe ON".format(channel))
        
    def TurnOff(self, channel = 1):
        self.inst.write("OUTPut{}:STATe OFF".format(channel))
        
    def GetFrequency(self, channel = 1):
        return self.inst.query('SOURce{}:FREQuency?'.format(channel))
        
    def SetFrequency(self, freq, channel = 1): #gen.SetFrequency('5 kHz') o por default en Hz
        self.inst.write("SOURce{}:FREQuency {}".format(channel,freq))
    
    def GetShape(self, channel = 1):
        return self.inst.query('SOURce{}:FUNCtion:SHAPe?'.format(channel))
    
    def SetShape(self, shape, channel = 1): #gen.SetShape('SQUare')
        self.inst.write("SOURce{}:FUNCtion {}".format(channel,shape)) 
    
    def GetVoltage(self, channel = 1):
        return self.inst.query('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude?'.format(channel))
    
    def SetVoltage(self, voltage, channel = 1): #gen.SetVoltage(2) Vpp
        self.inst.write('SOURce{}:VOLTage:LEVel:IMMediate:AMPLitude {}'.format(channel, voltage))
        
    def GetOffset(self, channel = 1):
        return self.inst.query('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet?'.format(channel))        
    
    def SetOffset(self, offset, channel = 1): #gen.SetOffset(1) V
        self.inst.write('SOURce{}:VOLTage:LEVel:IMMediate:OFFSet {}'.format(channel, offset))        
    
    def GeneralSet(self, freq, voltage, offset = '0 V', shape = 'SIN', channel = 1):
        self.SetFrequency(freq, channel)
        self.SetVoltage(voltage, channel)
        self.SetOffset(offset, channel)
        self.SetShape(shape, channel)
    
    def DiscreteSweep(self, freqini, frecfin, step, timeoff = 1,  channel = 1):
        Frequencies = np.array(float(freqini.split(" ")[0]), float(frecfin.split(" ")[0]), float(step.split(" ")[0]))
        #esto es por si el input lo consideramos como "2 kHz" o algo así. el split separa un string
        #en partes, dependiendo del separador (en este caso el separador es un espacio).
        for Fr in Frequencies:
            self.inst.write("SOURce{}:FREQuency {} {}".format(channel, Fr, freqini.split(" ")[1]))
            time.sleep(timeoff)
        
    def ContinuosSweep(self, freqini, freqfin, sweeptime, sweeptype = "LINear", channel = 1):
        self.inst.write('SOURce{}:SWEep:SPACing {}'.format(channel, sweeptype))
        self.inst.write('SOURce{}:SWEep:TIME {}'.format(channel, sweeptime))    
        self.inst.write('SOURce{}:FREQuency:STARt {}'.format(channel, freqini))
        self.inst.write('SOURce{}:FREQuency:STOP {}'.format(channel, freqfin))
        
        
        
class Osciloscopio():

    def __init__(self,num_osciloscopio = 0):
        self.rm = pyvisa.ResourceManager()
        self.lista = self.rm.list_resources()
        self.osciloscopios = []
        for i in range( 0 , len(self.lista)):   # Selecciona un Tektronix
           
            if self.lista[i][6:21]=='0x0699::0x0363:': # Seleccionamos elemento i desde caracter 6 al 20  cuyo 'Fabricante :: Modelo::' coincidan
                self.osciloscopios.append(self.lista[i])
                
                
        if self.osciloscopios == []:
            print('No hay osciloscopios conectados')        
            
        self.inst = self.rm.open_resource(self.osciloscopios[num_osciloscopio])  # Abre el primer instrumento de la lista
    
        
    def data_encdg_ascii(self):
        self.inst.write('DATA:ENCDG ASCII')
        
    def data_encdg_bin(self):
        self.inst.write('DATA:ENCDG RIBinary')

    def get_data_ascii(self):
        self.data_encdg_ascii()
        read = self.inst.query_ascii_values('CURVe?')
        
        plt.plot(read)
        plt.show()
        
        return read
        
        plt.plot(read)
        plt.show()
        
        return read

    def read_voltage(self):
        
        self.data_encdg_bin()
        read = np.array(self.inst.query_binary_values('CURVe?', datatype = 'b', is_big_endian= True))
        
        ymult = self.inst.query_ascii_values('WFMPRE:YMULT?') #Vertical scale factor
        yzero = self.inst.query_ascii_values('WFMPRE:YZERO?') #Offset Voltage
        yoff = self.inst.query_ascii_values('WFMPRE:YOFF?')   #Vertical Offset

        voltage = yzero + ymult*(read - yoff)
        
       # plt.plot(voltage)
        #plt.show()
        
        return voltage
    
       
    def read_time(self):    
        xincr = self.inst.query_ascii_values('WFMPRE:XINCR?') #Horizontal sampling interval
        xzero = self.inst.query_ascii_values('WFMPRE:XZERO?')
        pt_off = self.inst.query_ascii_values('WFMPRE:PT_Off?')
        
        n = np.linspace(0,2500,2500)
        #Ver https://www.i3detroit.org/wi/images/2/2d/460-ProgrammerManual.pdf pag 2-43
        time = xzero + xincr*(n - pt_off)
        
        return time
    
    def grafico(self):
        voltage = self.read_voltage()
        time = self.read_time()
        
        vpp = 2*max(voltage)
        
        plt.plot(time, voltage)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.show()
        
        return vpp

    
    def set_timebase(self, seconds):
        self.inst.write('HOR:DEL:SCA {}'.format(seconds))    
    
    
#%%
        
genfun= GeneradorFunciones()
osci = Osciloscopio()

genfun.SetFrequency(10)
