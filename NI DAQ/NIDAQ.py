# -*- coding: utf-8 -*-
"""
Created on Sun May 26 17:00:52 2019

@author: Pato
"""
import nidaqmx
from lantz import Feat

class NIDAQ ():
    def __init__(self, port=1,Time_Out=10, device_no=0):#, adq_type='CONTINUOUS'):
        self.port = port
        self.device_no = device_no
        self.Time_Out = Time_Out
#        self.adq_type = adq_type
        '''estos dos renglones que queden en una funcion que solo tenga el nombre del device
        y que sea una propiedad del objeto
        por ejemplo que guarde en self.device_no el numero del dispositivo, sin que el usuario
        tenga que elegirlo.'''
        self.system = nidaqmx.system.System.local()
        self.device_list = self.system.devices.device_names
        
    '''
    CONSULTAS!!!
    Self son los atributos prppios del objeto. Es para que el objeto sepa que es propio.
    Algo que este escrito como self.(algo) implica que el objeto sabe cuanto vale.
    
    No entiendo si por ejemplo cuando escribo voltaje tengo que escribir el self. No hace falta
    escribir self.voltaje salvo que yo quiera que el objeto recuerde cuanto vale voltaje.
   
    Otra cosa que pense es dar en init una opción donde figure como esta conectado todo si por NRSE,RSE O DIFF, pero no se si 
    conviene tomar un input con 3 opciones o armar 3 funciones distintas cada una con ese formato especificado.
    La mejor forma de hacerlo es darle un input donde yo escribo de que manera esta conectado, y que si escribo
    cualquier cosa me devuelva un error diciendome cuales son las 3 opciones de input posible. 
    
    Despues, la linea with nidaqmx.Task() as task no se puede agregar al init como self.nidaqmx.Task() as task y despues
    en cada funcion (cada función es un metodo) solo escribo with self.task:  
    No, meter el task como un decorador.
    '''    
    
    def getvoltage_ai_NRSE(self,sample_no,sample_rate):
        with nidaqmx.Task() as task: 
            # Port es una lista con los puertos y lo recorro para medir en simultaneo
            for i in self.port: 
                task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],i),terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
                task.timing.cfg_samp_clk_timing(sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.self.adq_type)
            
            voltaje = task.read(number_of_samples_per_channel = sample_no,timeout=self.Time_Out)
        
        return voltaje
    
    
    def getvoltage_ai_RSE(self,sample_no,sample_rate):
        with nidaqmx.Task() as task:
            # Port es una lista con los puertos y lo recorro para medir en simultaneo
            for i in self.port: 
                task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],i),terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
                task.timing.cfg_samp_clk_timing(sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.self.adq_type)
            voltaje = task.read(number_of_samples_per_channel = sample_no,timeout=self.Time_Out)
        
        return voltaje
    
    
    def getvoltage_ai_DIFF(self,sample_no,sample_rate,Samples_per_Channel):
        with nidaqmx.Task() as task:
            # Port es una lista con los puertos y lo recorro para medir en simultaneo
            for i in self.port: 
                task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],i),terminal_config=nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL)
                task.timing.cfg_samp_clk_timing(sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.FINITE,samps_per_chan=Samples_per_Channel)
            voltaje = task.read(number_of_samples_per_channel = sample_no,timeout=self.Time_Out)
        return voltaje
    
    
#    def samples_per_channel_ai_NRSE(self,sample_no):
#        with nidaqmx.Task() as task: 
#            task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],self.port),terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE)
#            cuentas = task.read(number_of_samples_per_channel=sample_no)
#        return cuentas
#    
    '''Esto me parece que hace exactamente lo mismo que las funciones get voltage '''
#    def samples_per_channel_ai_RSE(self,sample_no):
#        with nidaqmx.Task() as task:
#            # Port es una lista con los puertos y lo recorro para medir en simultaneo
#            for i in self.port: 
#                task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],i),terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)
#            cuentas = task.read(number_of_samples_per_channel=sample_no)
#        return cuentas
#    
#    
#    def samples_per_channel_ai_DIFF(self,sample_no):
#        with nidaqmx.Task() as task: 
#            # Port es una lista con los puertos y lo recorro para medir en simultaneo
#            for i in self.port: 
#                task.ai_channels.add_ai_voltage_chan("{}/ai{}".format(self.device_list[self.device_no],i),terminal_config=nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL)
#            cuentas = task.read(number_of_samples_per_channel=sample_no,timeout = self.Time_Out)
#        return cuentas
#    
    
    def samples_per_channel_di(self,linea_inicial,linea_final,sample_no,sample_rate):    
        from nidaqmx.constants import LineGrouping
        with nidaqmx.Task() as task:
            task.timing.cfg_samp_clk_timing(sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.self.adq_type)
            task.di_channels.add_di_chan("{}/port{}/line{}:{}".format(self.device_list[self.device_no],self.port,linea_inicial,linea_final), line_grouping=LineGrouping.CHAN_PER_LINE)
            cuentas = task.read(number_of_samples_per_channel=sample_no)
        return cuentas
    
    
    
    # Esto vendría a ser el equivalente al digital output pero manda un pulso. 
    def do_pulse(self,ctr,h_t,l_t,sample_rate):  
        from nidaqmx.types import CtrTime
        with nidaqmx.Task() as task:
            task.timing.cfg_samp_clk_timing(sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.self.adq_type)
            task.co_channels.add_co_pulse_chan_time(counter="{}/ctr{}".format(self.device_list[self.device_no],ctr),
                                                low_time=l_t,
                                                high_time=h_t)
            task.start()
        return 
    
    #Los datos pueden entrar como array en 1/2 D o como lista
    
    def setvoltage_ao(self,data,sample_rate):
        with nidaqmx.Task() as task:
            task.timing.cfg_samp_clk_timing(sample_rate,sample_mode=nidaqmx.constants.AcquisitionType.self.adq_type)
            task.ao_channels.add_ao_voltage_chan("{}/ao{}".format(self.device_list[self.device_no],self.port))
            task.write(data, auto_start=True)
        return 
    