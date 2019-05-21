# -*- coding: utf-8 -*-
"""
Created on Tue May 21 19:29:05 2019

@author: Publico
"""
import matplotlib.pyplot as plt
#def MedxCan_ai(n_cuentas_por_canal, puerto = 'ai1' ,n_disp = 0):
import nidaqmx as ni
# Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
system = ni.system.System.local()
lista_disp = system.devices.device_names
# Agrega un canal de input de voltaje analogico y devuelve la cantidad de mediciones pedidas
with ni.Task() as task: 
    task.ai_channels.add_ai_voltage_chan("{}/{}".format(lista_disp[n_disp],puerto),terminal_config=ni.constants.TerminalConfiguration.NRSE)
    
    Cuentas = task.read(number_of_samples_per_channel=n_cuentas_por_canal)
        
#    return Cuentas







cuentas=MedxCan_ai(15000)

plt.plot(cuentas)


