# -*- coding: utf-8 -*-
"""
Created on Sun May 26 17:00:52 2019

@author: Pato
"""
import nidaqmx

class NIDAQ ():
    def __init__(self, port, device_no=0):
        self.port = port
        self.device_no = device_no
        self.system = nidaqmx.system.System.local()
        self.device_list = self.system.devices.device_names
        
    '''
    CONSULTAS!!!
    
    No entiendo si por ejemplo cuando escribo voltaje tengo que escribir el self
   
    Y tampoco estoy entendiendo que es lo que hace el self
    
    Otra cosa que pense es dar en init una opción donde figure como esta conectado todo si por NRSE,RSE O DIFF, pero no se si 
    conviene tomar un input con 3 opciones o armar 3 funciones distintas cada una con ese formato especificado
    
    Despues, la linea with nidaqmx.Task() as task no se puede agregar al init como self.nidaqmx.Task() as task y despues
    en cada funcion (cada función es un metodo o el conjunto de funciones es el método?) solo escribo with self.task:  
    '''    
    
    def getvoltage_ai_NRSE(self):
        with nidaqmx.Task() as task: 
            task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
            voltaje = task.read()
        
        return voltaje

    def getvoltage_ai_RSE(self):
        with nidaqmx.Task() as task: 
            task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
            voltaje = task.read()
        
        return voltaje
    
    def getvoltage_ai_DIFF(self):
        with nidaqmx.Task() as task: 
            task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.DIFF)
            voltaje = task.read()
        return voltaje
    
    def samples_per_channel_ai_NRSE(self,sample_no):
        with nidaqmx.Task() as task: 
            task.ai_channels.add_ai_voltage_chan("{}/{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
            cuentas = task.read(number_of_samples_per_channel=sample_no)
        return cuentas
    
    def samples_per_channel_ai_RSE(self,sample_no):
        with nidaqmx.Task() as task: 
            task.ai_channels.add_ai_voltage_chan("{}/{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
            cuentas = task.read(number_of_samples_per_channel=sample_no)
        return cuentas
    
    def samples_per_channel_ai_DIFF(self,sample_no):
        with nidaqmx.Task() as task: 
            task.ai_channels.add_ai_voltage_chan("{}/{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.DIFF)
            cuentas = task.read(number_of_samples_per_channel=sample_no)
        return cuentas
    
    def samples_per_channel_di(self,linea_inicial,linea_final,sample_no):    
    
        from nidaqmx.constants import LineGrouping
        with nidaqmx.Task() as task:
            task.di_channels.add_di_chan("{}/port{}/line{}:{}".format(self.device_list[self.device_no],self.port,linea_inicial,linea_final), line_grouping=LineGrouping.CHAN_PER_LINE)
            cuentas = task.read(number_of_samples_per_channel=sample_no)
        return cuentas
    
    # Esto vendría a ser el equivalente al digital output pero manda un pulso. 
    def do_pulse(self,ctr,h_t,l_t):  
        from nidaqmx.types import CtrTime
        with nidaqmx.Task() as task:
            task.co_channels.add_co_pulse_chan_time(counter="{}/ctr{}".format(self.device_list[self.device_no],ctr),
                                                low_time=l_t,
                                                high_time=h_t)
            task.start()
        return 
    
    #Los datos pueden entrar como array en 1/2 D o como lista
    def setvoltage_ao(self,data):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan("{}/ao{}".format(self.device_list[self.device_no],self.port))
            task.write(data, auto_start=True)
        return 


    
            
       