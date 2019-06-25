# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:02:27 2019

@author: Publico
"""

from lantz.ino import INODriver, BoolFeat, QuantityFeat, BoolDictFeat, QuantityDictFeat
from lantz.qt import Backend, Frontend, InstrumentSlot

class FLOWPIDDriver(INODriver):
        
#    def __init__(self,Kp,Ki,Kd,Set_Point):
#        self.Kp = Kp
#        self.Ki = Ki
#        self.Kd = Kd
#        self.Set_Point = Set_Point
        
    control_loop_enabled=BoolFeat('Control_Loop_enabled')
    Kp=QuantityFeat('Kp')
    Ki=QuantityFeat('Ki')
    Kd=QuantityFeat('Kd')
    set_point=QuantityFeat('Set_Point', units='L/hour')
    flow_value = QuantityFeat('Flow', units = 'L/hour', setter=False) # Si agrego este argumento: setter=False, entonces la funcion en el sketch de Arduino se genera sin setter.
#    valve_opened = BoolDictFeat('Valve_Opened', keys=(1, 2))
    pump_flow = QuantityDictFeat('Pump_Flow', keys=(1, 2) , units = 'L/hour')
    
   
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
#    def set_Ki(self):
#        self.board.Kp = self.board.Ki
#        
#    def set_Kd(self):
#        self.board.Kp = self.board.Kd
#        
#    def set_set_point(self):
#        self.board.set_point = self.board.Set_Point
#        
##    def open_valve(self,no):
##        self.board.valve_opened[no]= True
##
##    def close_valve(self,no):
##        self.board.valve_opened[no]= False
#        
#        
#    def get_flow(self):
#        print(self.board.flow_value)
#        
#    def set_flow(self,Flow_Value):
#        self.board.flow_value = self.board.flow
#        
#    
#            
#
#'''De la misma manera que tenia dos opcines para definir la funcion, tengo dos
#opciones para definir que hace esa funcion '''        
#        
##    def open_valve_1_method(self):
##        self.board.valve_1_opened = True
##   
##    def close_valve_1_method(self):
##        self.board.valve_1_opened = False
##
##    def open_valve_2_method(self):
##        self.board.valve_2_opened = True
##        
##    def close_valve_2_method(self):
##        self.board.valve_2_opened = False
##        
#    
#
#class FLOWPIDUserInterfase(Frontend):
#    gui = 'FLOWPID.ui'
#
#    def connect_backend(self):
#        super().connect_backend()
#        self.widget.enable_control_loop_button.clicked.connect(self.backend.enable_control_loop_method)
#        self.widget.disable_control_loop_button.clicked.connect(self.backend.disable_control_loop_method)
##        self.widget.open_valve_1_button.clicked.connect(self.backend.open_valve_1_method)
##        self.widget.close_valve_1_button.clicked.connect(self.backend.close_valve_1_method)
##        self.widget.open_valve_2_button.clicked.connect(self.backend.open_valve_2_method)
##        self.widget.close_valve_2_button.clicked.connect(self.backend.close_valve_2_method)
#        
#
#
#if __name__ == '__main__':
#    from lantz.core.log import log_to_screen, log_to_socket, DEBUG
#    from lantz.qt import start_gui_app, wrap_driver_cls
#    
#    # ~ log_to_socket(DEBUG) # Uncommment this line to log to socket
#    log_to_screen(DEBUG) # or comment this line to stop logging
#
#    QFLOWPID = wrap_driver_cls(FLOWPIDDriver)
#    with QFLOWPID.via_packfile('FLOWPIDDriver.pack.yaml', check_update=True) as board:
#        app = FLOWPIDBackend(board=board)
#        start_gui_app(app, FLOWPIDUserInterfase)

if __name__ == '__main__':
    from lantz.core.log import log_to_screen, log_to_socket, DEBUG
    from lantz.qt import start_gui_app, wrap_driver_cls
    from lantz import ureg
    
    # ~ log_to_socket(DEBUG) # Uncommment this line to log to socket
    log_to_screen(DEBUG) # or comment this line to stop logging

    with FLOWPIDDriver.via_packfile('FLOWPIDDriver.pack.yaml', check_update=True) as board:
        board.set_point = 90 * ureg.liter/ureg.hour
        print(board.set_point)