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
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time

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
    
    @Feat() # devuelve el nombre de la forma
    def shape(self, channel = 1):
        return self.query('SOURce{}:FUNCtion:SHAPe?'.format(channel))
    
    @shape.setter
    def shape(self, shape, channel = 1): #gen.SetShape('SQUare')
        self.write("SOURce{}:FUNCtion {}".format(channel,shape)) 

     

# Armarmos un barrido en frecuencias
    
f_min = 1
f_max = 20000    
log_f_min = np.log10(f_min)
log_f_max = np.log10(f_max)
n = 20 # cantidad de pasos
#val_paso= (f_max - f_min)/n
freqs = np.logspace(log_f_min,log_f_max,num=n+1,base=10)
A = 0.3   # valor de amplitud a utilizar en V
cant_periodos = 20

# Establecemos condiciones para grabar 

CHUNK = 1024  # CAntidad de frames por buffer
FORMAT = pyaudio.paInt16  # SI CAMBIO EL TIPO DE DATO CAMBIAR EL VARIABLE AUDIO
CHANNELS = 1
RATE = 96000  # Usamos esta frecuencia para tener suficientes puntos para frecuencias altas

# WAVE_OUTPUT_FILENAME = "output.wav"
 
p = pyaudio.PyAudio()  # Configura el sistema de PortAudio

for index in range(p.get_device_count()):   
    print(p.get_device_info_by_index(index)) 
    
# El for anterior, busca cuantos aparatos hay conectados y luego los lista
# especificando cual es cada uno

with GeneradorFunciones.via_usb(serialno) as genfun:
    
    genfun.voltage = A # Amplitud constante 
    
    amplitud_medida = []
    
    k = 0
    
    for i in freqs:
        genfun.frequency = i
        RECORD_SECONDS = max(0.3,cant_periodos/i)
        k = k+1
        '''
Esto abre un flujo en determinado aparato, con  ciertos parametros de 
audio, para poder grabar o reproducir audio. Es decir, Configura
 p.Stream para reproducir o grabar audio
'''

        print("* recording aprox {} seg" .format(int(RECORD_SECONDS)))
 
        stream = p.open(format=FORMAT,     # Tipos de formato paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat   
                channels=CHANNELS,  #  Numero de canales
                rate=RATE,          #  frecuencia de muestreo
                input=True,   #   Especifica si es un input stream. Defecto = False
                frames_per_buffer=CHUNK, # Cantidad de frames por buffer
                input_device_index=1)  # Indice del dispositivo a usar. Si no especifico usa el por defecto y lo ignora si el input es 'False'
         

        frames = []
 
 
        for j in range(0, int( (RATE / CHUNK) * RECORD_SECONDS)):  # Si el numero es chico como usa la funcion int redondea a cero y no da nada.
            data = stream.read(CHUNK)  # Lee la data del audio del stream CHUNK
            frames.append(data)
 
 
        print("* done recording {}" .format(k))
 
        stream.stop_stream()   # Pausa la grabacion
        stream.close()     # termina el stream
 
        audio = np.frombuffer(b''.join(frames),dtype=np.int16)
        
        amplitud_medida.append(max(audio))
        
#        time.sleep(0.3)
    
    plt.figure(1)
    plt.plot(freqs,amplitud_medida)
    plt.show()
    plt.figure(2)
    t = np.linspace(0,RECORD_SECONDS,num=audio.size)
    plt.plot(t,audio)
    plt.show()

p.terminate()    # termina la sesion de pyaudio    