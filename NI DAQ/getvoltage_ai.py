# -*- coding: utf-8 -*-
"""
Created on Tue May 21 15:33:04 2019

@author: Publico
"""
# la variable puerto debe ser un string y el dispositivo por defecto es el primero que encuentre
def getvoltage_ai(puerto,n_disp = 0):
#    puerto='ai1'
#    n_cuentas_por_canal=5
#    n_disp = 0
    import nidaqmx as ni
    # Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
    system = ni.system.System.local()
    lista_disp = system.devices.device_names
    # Agrega un canal de input de voltaje analogico y mide cuanto vale
    with ni.Task() as task: 
        task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(lista_disp[n_disp],puerto),terminal_config=ni.constants.TerminalConfiguration.NRSE)
        voltaje = task.read()
        
    return voltaje

#%%
def MedxCan_ai(n_cuentas_por_canal, puerto = 'ai1' ,n_disp = 0):
    import nidaqmx as ni
    # Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
    system = ni.system.System.local()
    lista_disp = system.devices.device_names
    # Agrega un canal de input de voltaje analogico y devuelve la cantidad de mediciones pedidas
    with ni.Task() as task: 
        task.ai_channels.add_ai_voltage_chan("{}/{}".format(lista_disp[n_disp],puerto),terminal_config=ni.constants.TerminalConfiguration.NRSE)
        Cuentas = task.read(number_of_samples_per_channel=n_cuentas_por_canal)
        
    return Cuentas

#%%
    
# Esta funcion crea un canal digital de input y dado un device, un puerto y la linea o lineas correspondientes
# al puerto, mide una cierta cantidad de cuentas por canal 
def MedxCan_di(n_puerto,linea_inicial,linea_final,samples_per_channel,n_disp=0):    
    import nidaqmx
    # Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
    system = nidaqmx.system.System.local()
    lista_disp = system.devices.device_names
    from nidaqmx.constants import LineGrouping
    with nidaqmx.Task() as task:
        task.di_channels.add_di_chan("{}/port{}/line{}:{}".format(lista_disp[n_disp],n_puerto,linea_inicial,linea_final), line_grouping=LineGrouping.CHAN_PER_LINE)
        Cuentas = task.read(number_of_samples_per_channel=samples_per_channel)
    return Cuentas
      
#%%

## Esto vendrai a se equivalente al digital output 
#pareceria que manda un pulso 
def pulso(ctr ,h_t=0.001,l_t=0.001, n_disp = 0):
    import nidaqmx 
    from nidaqmx.types import CtrTime
    system = nidaqmx.system.System.local()
    lista_disp = system.devices.device_names
    with nidaqmx.Task() as task:
        task.co_channels.add_co_pulse_chan_time(counter="{}/ctr{}".format(lista_disp[n_disp],ctr),
                                                low_time=l_t,
                                                high_time=h_t)
        task.start()
    return 
        
#%%
#Los datos pueden entrar como array en 1/2 D o como lista
def setvoltage_ao(n_puerto,datos,n_disp = 0):
    import nidaqmx
    # Esta primera parte devuelve que dispositivos estan conectados y cual es el numero
    system = nidaqmx.system.System.local()
    lista_disp = system.devices.device_names
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan("{}/ao{}".format(lista_disp[n_disp],n_puerto))
        task.write(datos, auto_start=True)
    return 

#%%
    

    
            
       
            