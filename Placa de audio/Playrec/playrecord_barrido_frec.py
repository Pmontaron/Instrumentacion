# -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:33:12 2019

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
''' Seteo condiciones para realizar un barrido de frecuencia'''    

#duration = 10    # Duracion de la reproduccion y grabacion del sonido generado por la placa
fs = 44100       # Sampling rate
f_min = 1        # Frecuencia de inicio
f_max = 30000    # Frecuencia de finalizacion
log_f_min = np.log10(f_min)   # Tomo log base 10 de la frec minima
log_f_max = np.log10(f_max)   # log base 10 de la frec maxima
n = 20                        # cantidad de pasos
freqs = np.logspace(log_f_min,log_f_max,num=n+1,base=10)  # vector de frecuencias
cant_periodos = 20            # Cantidad de periodos deseados

''' Aca va guardado en forma de matriz los valores de la grabacion para cada paso (frecuencias). 
Cada paso corresponde a una fila de la matriz. ''' 

RawData=[]

''' Aca guardo la amplitud maxima para cada frecuencia '''
amplitud_medida = []


k = 0           # Genero un indice para saber en que paso estoy

for i in freqs:
    f= i
    duration = max(0.3,cant_periodos/i)
    t = np.linspace(0, duration, fs * duration)  #  Produce un vector tiempo de 'duration' segs
    y = np.sin(f * 2 * np.pi * t)  #  Genero un seno
    k = k+1
    
    print("* recording aprox {} seg" .format(int(duration)))
    
    '''Guardo la grabacion en myrecording. Usar 1 o 2 canales afecta la canitdad de 
    grabaciones que realiza.
    '''
    myrecording = sd.playrec(y,fs,channels=1,blocking=True)  
    RawData.append(myrecording)
    amplitud_medida.append(max(myrecording))
    
    print("* done recording {}" .format(k))



''' Ploteo en la figura 1 la amplitud en funcion de la frecuencia
y en la figura 2 la grabacion y el sonido emitido en el tiempo para la ultima frecuencia
si se quieren graficar para las otras frecuencias calculadas, hay que buscar para la 
frecuencia deseada el 'myrecording' apropiado en la variable 'RawData' '''

plt.figure(1)
plt.loglog(freqs,amplitud_medida)
plt.title('Barrido de frecuencia')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Amplitud')
plt.show()

''' Esta segunda parte, plotea el sonido grabado y el emitido para una frecuencia dada
en particular esta escrito para la frecuencia máxima que es la que queda al concluir el for'''

plt.figure(2)
plt.plot(t,myrecording, label = 'Sonido grabado para f={}' .format(f))
plt.plot(t,y, label = 'Sonido emitido para f={}' .format(f))
plt.title('Sonido emitido y grabado vs tiempo')
plt.xlabel('tiempo [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.show()



#%% 







