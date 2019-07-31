# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:02:27 2019

@author: Publico
"""

from lantz.ino import INODriver, BoolFeat, QuantityFeat, BoolDictFeat, QuantityDictFeat
from lantz.qt import Backend, Frontend, InstrumentSlot, QtCore
from lantz import Q_
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


#now = datetime.now() # current date and time

class FLOWPIDDriver(INODriver):
        
#    def __init__(self,Kp,Ki,Kd,Set_Point):
#        self.Kp = Kp
#        self.Ki = Ki
#        self.Kd = Kd
#        self.Set_Point = Set_Point
        
    cl=BoolFeat('CLEN')
    kp=QuantityFeat('KP')
    ki=QuantityFeat('KI')
    kd=QuantityFeat('KD')
    setpoint=QuantityFeat('SP', units='L/hour', limits = (60,1000))
    flowvalue = QuantityFeat('FV', units = 'L/hour', setter=False) # Si agrego este argumento: setter=False, entonces la funcion en el sketch de Arduino se genera sin setter.
#    valve_opened = BoolDictFeat('Valve_Opened', keys=(1, 2))
    pumpflow1 = QuantityFeat('PF1', units = 'L/hour' , limits = (0,102.5)) # trabaja entre 27 y 102.5 l/h 
    pumpflow2 = QuantityFeat('PF2', units = 'L/hour' , limits = (0,72.9)) # Trabaja entre 17.94 y 72.9 L/H
   
    # LOs valores de flujo negativo estan para que las bombas se apaguen
''' Hay dos maneras de escribir que las valvulas se puedan abrir o cerrar
en ambos casos conviene ser especifico con lo que hace la función. La primer 
forma consiste en dar dos funciones distintas, una para cada valvula que valga
true si esta abierta o false si la quiero cerrar. La otra forma es usar el 
BoolDictFeat para armar un diccionario entonces ademas de tomar los valores
True/False, toma los valores 1 o 2 dependiendo de que valvula quiero usar.  '''
#    valve_1_opened = BoolFeat('OPEN_VALVE_1')
#    vavle_2_opened = BoolFeat('OPEN_VALVE_2')
    
    
 
#
#class FLOWPIDBackend(Backend):
#    board: FLOWPIDDriver = InstrumentSlot
#    def enable_control_loop_method(self):
#        self.board.control_loop = True
#    
#    def disable_control_loop_method(self):
#        self.board.control_loop = False
#        
#    def set_Kp(self):
#        self.board.Kp = self.board.Kp
#
#    def get_Kp(self):
#        print(Kp)
#        
#    def set_Ki(self):
#        self.board.Ki = self.board.Ki
#        
#    def get_Ki(self):
#        print(Ki)
#        
#    def set_Kd(self):
#        self.board.Kd = self.board.Kd
#
#    def get_Kd(self):
#        print(Kd)
#        
#    def set_set_point(self):
#        self.board.set_point = self.board.Set_Point
#
#    def get_set_point(self):
#        print(self.board.Set_Point)
#        
#    def set_pump_flow(self,no):
#        self.board.pump_flow[no]= self.board.pump_flow[no]
#
#    def get_pump_flow(self,no):
#        print(self.board.pump_flow[no])
#        
#        
#    def get_flow(self):
#        print(self.board.flow_value)
#        
#    def set_flow(self,Flow_Value):
#        self.board.flow_value = self.board.flow
#        
#class FLOWPIDUserInterfase(Frontend):
#    gui = 'FLOWPID.ui'
#
#    def connect_backend(self):
#        super().connect_backend()
#        self.widget.enable_control_loop_button.clicked.connect(self.backend.enable_control_loop_method)
#        self.widget.disable_control_loop_button.clicked.connect(self.backend.disable_control_loop_method)



if __name__ == '__main__':
    #from lantz.core.log import log_to_screen, log_to_socket, DEBUG
    #from lantz.qt import start_gui_app, wrap_driver_cls, QtCore
    #import time
    
    # ~ log_to_socket(DEBUG) # Uncommment this line to log to socket
    #log_to_screen(DEBUG) # or comment this line to stop logging

    ''' Inicializamos el programa definiendo las variables'''

    board = FLOWPIDDriver.via_packfile('FLOWPIDDriver.pack.yaml', check_update=True)
    board.initialize()  
    
    print(board.kp)
    board.kp = 1
    print(board.kp)
    
    print(board.ki)
    board.ki = 0
    print(board.ki)
    
    print(board.kd)
    board.kd = 5
    print(board.kd)
    
    print(board.setpoint)
    board.setpoint = 0
    print(board.setpoint)
    
    print(board.cl)
    board.cl= False
    print(board.cl)
#    
    print(board.pumpflow1) 
    board.pumpflow1 = 70
    print(board.pumpflow1) 
    
    print(board.pumpflow2)
    
    board.pumpflow2 = 30
    print(board.pumpflow2) 
    
#    
#    print(board.flowvalue)
    
    board.setpoint = 80

#    board.pumpflow1= 0
#    board.pumpflow2 = 0
#    board.pumpflow1 = 70
#    board.pumpflow2 = 70  

 # Cantidad de segundos que quiero correr el programa dividios el paso de tiempo del sleep da el valor al que i debe ser menor para correr
    i = 1
    interval = 1
   # Tolerancia = 
    flow_data=[]
    t1_start = time.perf_counter()
    
    n=0
    while n<300:
        t1_stop = time.perf_counter()
        flow_data.append([board.flowvalue.m,board.pumpflow1.m,board.pumpflow2.m,t1_stop])
        t1_partial= time.perf_counter()
        time.sleep(interval)
        n=n+1
        
        
        
    t1_start = time.perf_counter()
    
    board.cl= True
    while i<1200:   
        t1_stop = time.perf_counter()
        flow_data.append([board.flowvalue.m,board.pumpflow1.m,board.pumpflow2.m,t1_stop])
        t1_partial= time.perf_counter()
        time.sleep(interval)
        i= i+1
        
    tiempo = []
    data = []
    for j in range(len(flow_data)):
        tiempo.append(flow_data[j][3]-flow_data[0][3])
        data.append(flow_data[j][0])
        
mean_flow = np.mean(data)
std_flow = np.std(data)
    
''' En esta parte de arriba, podemos medir en un intervalo de tiempo como cambia el flujo del caudalimetro, y de las bombas
con o sin pid.'''


#%% Esta parte sirve para graficar el flujo en función del tiempo sin el pid y con el flujo de bombas fijo

plt.plot(tiempo,data)
plt.title("Flujo bomba A = {} , Flujo bomba B = {}  ".format(board.pumpflow1 , board.pumpflow2))
plt.xlabel('tiempo [seg]')
plt.ylabel('flujo [L/h]')
plt.show()

#%% Esta parte sirve para graficar el flujo en función del tiempo para el PID

plt.figure()
plt.plot(tiempo,data)
plt.title("Set point = {} , KP = {} ; KI = {} ; KD = {} ".format(board.setpoint, board.kp, board.ki, board.kd))
plt.xlabel('tiempo [seg]')
plt.ylabel('flujo [L/h]')
plt.show()

# esta otra parte sirve para ver como varió el valor del flujo de las bombas durante el mismo tiempo

data_bombaA = []
data_bombaB = []

for j in range(len(flow_data)):
    data_bombaA.append(flow_data[j][1])
    data_bombaB.append(flow_data[j][2])
    
plt.figure()
plt.plot(tiempo,data_bombaA,label='Flujo A')
plt.plot(tiempo,data_bombaB, label= 'Flujo B')
plt.xlabel('tiempo [seg]')
plt.ylabel('flujo [L/h]')
plt.legend()
plt.show()

#%% Esta parte esta para analizar los datos achicandolos y filtrando cosas que no nos interesan



data_estable = data[100:500]

plt.plot(tiempo[100:500],data_estable)
plt.title("Flujo B1= 102L/H y Flujo B2 = 70 L/h")
plt.xlabel('tiempo [seg]')
plt.ylabel('flujo [L/h]')
plt.show()

mean_flow_estable = np.mean(data_estable)
std_flow_estable = np.std(data_estable)