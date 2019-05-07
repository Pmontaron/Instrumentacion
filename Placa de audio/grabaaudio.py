# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:24:15 2019

@author: macabre
"""

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
 
CHUNK = 1024  # CAntidad de frames por buffer
FORMAT = pyaudio.paInt16  # SI CAMBIO EL TIPO DE DATO CAMBIAR EL VARIABLE AUDIO
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.01951232399646889

WAVE_OUTPUT_FILENAME = "output.wav"
 
p = pyaudio.PyAudio()  # Configura el sistema de PortAudio
'''


print("Input Device Info")
print(p.get_default_input_device_info())
print("Output Device Info")
print(p.get_default_output_device_info())
 
for i in range(p.get_host_api_count()):
    print(p.get_host_api_info_by_index(i))
'''
for index in range(p.get_device_count()):   
    print(p.get_device_info_by_index(index)) 
    
# El for anterior, busca cuantos aparatos hay conectados y luego los lista
# especificando cual es cada uno

'''
Esto abre un flujo en determinado aparato, con  ciertos parametros de 
audio, para poder grabar o reproducir audio. Es decir, Configura
 p.Stream para reproducir o grabar audio
'''
stream = p.open(format=FORMAT,     # Tipos de formato paFloat32, paInt32, paInt24, paInt16, paInt8, paUInt8, paCustomFormat   
                channels=CHANNELS,  #  Numero de canales
                rate=RATE,          #  frecuencia de muestreo
                input=True,   #   Especifica si es un input stream. Defecto = False
                frames_per_buffer=CHUNK, # Cantidad de frames por buffer
                input_device_index=1)  # Indice del dispositivo a usar. Si no especifico usa el por defecto y lo ignora si el input es 'False'
 
print("* recording")
 
frames = []
 
 
for i in range(0, int( (RATE / CHUNK) * RECORD_SECONDS)):  # Si el numero es chico como usa la funcion int redondea a cero y no da nada.
    data = stream.read(CHUNK)  # Lee la data del audio del stream CHUNK
    frames.append(data)
 
 
print("* done recording")
 
stream.stop_stream()   # Pausa la grabacion
stream.close()     # termina el stream
p.terminate()    # termina la sesion de portaudio
 
time = []
 
 
audio = np.fromstring(b''.join(frames),dtype=np.int16)
#audio = np.fromstring(b''.join(frames),dtype=np.float64)
 
t = np.linspace(0,RECORD_SECONDS,num=audio.size)
plt.plot(t,audio)
plt.show()