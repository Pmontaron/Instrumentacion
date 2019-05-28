# -*- coding: utf-8 -*-
"""
Created on Thu May 23 06:36:10 2019

@author: Publico
"""


# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:23:26 2019
@author: Publico
"""

#Primero vemos que elementos estan conectados y abrimos el generador de 
# funciones para hallar su numero de serie
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

serialno =inst.query("*IDN?")[19:26]



#%%
from lantz import MessageBasedDriver, Feat
import numpy as np
import matplotlib.pyplot as plt


#from lantz.log import log_to_screen, DEBUG
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


    @Feat()
    def frequency(self, channel = 1): #frequency('numero') te devuelve la frequencia del canal 'numero'
        return float(self.query('SOURce{}:FREQuency?'.format(channel)))
    
    @frequency.setter
    def frequency(self, freq, channel = 1): #frequency ='5 kHz' o por default en Hz te setea la frequencia
        self.write("SOURce{}:FREQuency {}".format(channel,freq))
#    
#    @Feat() # devuelve el nombre de la forma
#    def shape(self, channel = 1):
#        return self.query('SOURce{}:FUNCtion:SHAPe?'.format(channel))
#    
#    @shape.setter
#    def shape(self, shape, channel = 1): #gen.SetShape('SQUare')
#        self.write("SOURce{}:FUNCtion {}".format(channel,shape)) 

#%%     

# Armarmos un barrido en frecuencias
    
n = 40 # cantidad de pasos
#val_paso= (f_max - f_min)/n
freqs = np.linspace(250,10000,num=n)
A = 1   # valor de amplitud a utilizar en V

RawData=[]
#import matplotlib.pyplot as plt
import numpy as np
import nidaqmx as ni

with GeneradorFunciones.via_usb(serialno) as genfun:
    
    genfun.voltage = A # Amplitud constante 
    
    amplitud_medida = []
    
    k = 0
    
    for i in freqs:
        genfun.frequency = i
        n_disp=0
        puerto='ai1'
        T=1
        n_cuentas_por_canal=10000*T
        # Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
        system = ni.system.System.local()
        lista_disp = system.devices.device_names
        # Agrega un canal de input de voltaje analogico y devuelve la cantidad de mediciones pedidas

        with ni.Task() as task: 
            task.ai_channels.add_ai_voltage_chan(("{}/{}".format(lista_disp[n_disp],puerto),"Dev0/ai2",terminal_config=ni.constants.TerminalConfiguration.DIFFERENTIAL)
            task.timing.cfg_samp_clk_timing(10000,sample_mode=ni.constants.AcquisitionType.CONTINUOUS) #seteo la frecuencia de muestreo en 10kHz y que adquiera de forma continua, necesito
            cuentas = task.read(number_of_samples_per_channel=n_cuentas_por_canal)
        RawData.append(cuentas)
 
   
  
#%%
#n_disp=0
#puerto='ai1'
#T=1
#n_cuentas_por_canal=10000*T
#import matplotlib.pyplot as plt
#import numpy as np
##def MedxCan_ai(n_cuentas_por_canal, puerto = 'ai1' ,n_disp = 0):
#import nidaqmx as ni
## Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
#system = ni.system.System.local()
#lista_disp = system.devices.device_names
## Agrega un canal de input de voltaje analogico y devuelve la cantidad de mediciones pedidas
#
#with ni.Task() as task: 
#    task.ai_channels.add_ai_voltage_chan("{}/{}".format(lista_disp[n_disp],puerto),terminal_config=ni.constants.TerminalConfiguration.NRSE)
#    task.timing.cfg_samp_clk_timing(10000,sample_mode=ni.constants.AcquisitionType.CONTINUOUS) #seteo la frecuencia de muestreo en 10kHz y que adquiera de forma continua, necesito
#    cuentas = task.read(number_of_samples_per_channel=n_cuentas_por_canal)
#        
##    return Cuentas
##
##
##
##
##cuentas=MedxCan_ai(15000)
        
t=np.linspace(0,T,T*10000)
t0=np.linspace(0,T,T*100000)
plt.plot(t,RawData[0])
plt.plot(t0,0.2*np.sin(t0*2*np.pi*5000.0))
