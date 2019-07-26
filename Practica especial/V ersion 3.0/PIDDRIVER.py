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
    setpoint=QuantityFeat('SP', units='L/hour')
    flowvalue = QuantityFeat('FV', units = 'L/hour', setter=False) # Si agrego este argumento: setter=False, entonces la funcion en el sketch de Arduino se genera sin setter.
#    valve_opened = BoolDictFeat('Valve_Opened', keys=(1, 2))
    pumpflow1 = QuantityFeat('PF1', units = 'L/hour' , limits = (0,77))
    pumpflow2 = QuantityFeat('PF2', units = 'L/hour' , limits = (0,77))
   
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
    board.kd = 0
    print(board.kd)
    
    print(board.setpoint)
    board.setpoint = 0
    print(board.setpoint)
    
    print(board.cl)
    board.cl= False
    print(board.cl)
#    
    print(board.pumpflow1) 
    board.pumpflow1 = 0
    print(board.pumpflow1) 
    
    print(board.pumpflow2)
    
    board.pumpflow2 = 0
    print(board.pumpflow2) 
    
#    
#    print(board.flowvalue)
    
    

    board.setpoint = 100
    board.cl= True
    board.pumpflow1 = 70
    board.pumpflow2 = 70

    # esta parte del programa debería medir el flujo para el pid 
    interval = 1
    Tolerancia = (0.2426513536134539)*60
    flow_data=[]
    i = 0.01
    while i<100:    
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
        
    plt.plot(tiempo,data)
    plt.title("Flujo de bombas fijo 60 L/h")
    plt.xlabel('tiempo [seg]')
    plt.ylabel('flujo [L/h]')
    plt.show()
    
#%% 
    ''' Guardamos los valores de flujo por el caudalimetro en intervalos
    de X ms. '''  
    
#    board.timer = QtCore.QTimer()
#    board.timer.setInterval(interval) # ms
#    i=1
#        board.cl = True
#    board.timer.timeout.connect(flow_data.append([board.flowvalue,interval*i,board.pumpflow1,board.pumpflow2]))
  
    ''' Armar un programa que mida el flujo del caudalimetro durante cierto tiempo '''
 # Cantidad de segundos que quiero correr el programa dividios el paso de tiempo del sleep da el valor al que i debe ser menor para correr
    i = 1
    interval= 0.1
    flow_data=[]
    t1_start = time.perf_counter()
    while i<9000:
        t1_stop = time.perf_counter()
        #Hora=datetime.now().strftime('%H:%M:%S.%f')[:-4]
        flow_data.append([board.flowvalue.m,board.pumpflow1.m,board.pumpflow2.m,t1_stop])
        time.sleep(interval)
        t1_partial= time.perf_counter()
        i=i+1
        
    tiempo = []
    data = []
    for j in range(len(flow_data)):
        tiempo.append(flow_data[j][3]-flow_data[0][3])
        data.append(flow_data[j][0])
        
    plt.plot(tiempo,data)
    plt.title("Flujo de bombas fijo 60 L/h")
    plt.xlabel('tiempo [seg]')
    plt.ylabel('flujo [L/h]')
    plt.show()

#%%
#Ahora empezamos a realizar las mediciones. Primero tenemos que tomar distintos valorse de flujo para Kp = 1  Ki=Kd=0 
#y graficarlo y despues vamos probando con otras constantes.    



    
#    init=datetime.now().strftime('%M:%S.%f')[:-4]
#    while cont<10:
#        actual=datetime.now().strftime('%M:%S.%f')[:-4]
#        time=(float(actual[0:1])*60+float(actual[3:len(init)]))-(float(init[0:1])*60+float(init[3:len(init)]))
#        flow_data.append([board.flowvalue.m,time,board.pumpflow1.m,board.pumpflow2.m])
#        if abs(board.flowvalue.m - board.setpoint.m)<Tolerancia:
#            cont=cont+1
#        else:
#            cont=0
#        time.sleep(interval)