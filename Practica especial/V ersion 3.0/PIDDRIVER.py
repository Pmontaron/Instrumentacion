# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:02:27 2019

@author: Publico
"""

from lantz.ino import INODriver, BoolFeat, QuantityFeat, BoolDictFeat, QuantityDictFeat
from lantz.qt import Backend, Frontend, InstrumentSlot, QtCore
from lantz import Q_

class FLOWPIDDriver(INODriver):
        
#    def __init__(self,Kp,Ki,Kd,Set_Point):
#        self.Kp = Kp
#        self.Ki = Ki
#        self.Kd = Kd
#        self.Set_Point = Set_Point
        
    CLENABLE=BoolFeat('CLENABLE')
    kp=QuantityFeat('KP')
    ki=QuantityFeat('LI')
    kd=QuantityFeat('KD')
    setpoint=QuantityFeat('SP', units='L/hour')
    flowvalue = QuantityFeat('FV', units = 'L/hour', setter=False) # Si agrego este argumento: setter=False, entonces la funcion en el sketch de Arduino se genera sin setter.
#    valve_opened = BoolDictFeat('Valve_Opened', keys=(1, 2))
    pumpflowvalue1 = QuantityFeat('PF1', units = 'L/hour' , limits = (0,77))
    pumpflowvalue2 = QuantityFeat('PF2', units = 'L/hour' , limits = (0,77))
   
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
    board.kp = 1
    board.ki = 5
    board.kd = 3
#    board.Set_point = 0
#    board.control_loop_enabled= False
#    print(board.pump_flow[1]) 
#    print(board.pump_flow[2])
#    board.pump_flow[1]= Q_(0, 'liter/hour')
#    board.pump_flow[2] = Q_(100, 'liter/hour')
#
    ''' Guardamos los valores de flujo por el caudalimetro en intervalos
    de X ms. ''' 
    interval= 500
    flow_data=[]
    i=1
    board.timer = QtCore.QTimer()
    board.timer.setInterval(interval) # ms
    board.timer.timeout.connect(flow_data.append([board.flowvalue,interval*i,board.pumpflowvalue1,board.pumpflowvalue2]),i+1)
    
#    



