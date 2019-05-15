# -*- coding: utf-8 -*-
"""
Created on Wed May 15 17:35:43 2019

@author: Pato
"""

''' Previo a correr esto, revisar que para el volumen de line in / altavoz no sature
la señal usando el programa playrecord'''

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

'''Esto solo muestra los dispositivos conectados '''
p = pyaudio.PyAudio()  # Configura el sistema de PortAudio

for index in range(p.get_device_count()):   
    print(p.get_device_info_by_index(index)) 

#%%
''' Seteo condiciones para realizar un barrido de amplitud'''    

duration = 10    # Duracion de la reproduccion y grabacion del sonido generado por la placa
fs = 44100       # Sampling rate
f = 440           # Frecuencia de la onda generada
n = 20                        # cantidad de pasos
amp_inic = 0.01
amp_final = 1
amp = np.linspace(amp_inic,amp_final,n)  # Lista de amplitudes
cant_periodos = 20            # Cantidad de periodos deseados

''' Aca va guardado en forma de matriz los valores de la grabacion para cada paso (amplitud). 
Cada paso corresponde a una fila de la matriz. ''' 

RawData=[]

''' Aca guardo la amplitud maxima para cada frecuencia '''
amplitud_medida = []


k = 0           # Genero un indice para saber en que paso estoy

for i in amp:
    A = i 
    t = np.linspace(0, duration, fs * duration)  #  Produce un vector tiempo de 'duration' segs
    y = A * np.sin(f * 2 * np.pi * t)  #  Genero un seno
    k = k+1
    
    print("* recording aprox {} seg" .format(int(duration)))
    
    '''Guardo la grabacion en myrecording. Usar 1 o 2 canales afecta la canitdad de 
    grabaciones que realiza.
    '''
    myrecording = sd.playrec(y,fs,channels=1,blocking=True)  
    RawData.append(myrecording)
    amplitud_medida.append(max(myrecording))
    
    print("* done recording {}" .format(k))



''' Falta decidir que plotear '''













