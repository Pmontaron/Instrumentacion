# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:02:27 2019

@author: Publico
"""

import lantz.ino import INODriver, BoolFeat, QuantityFeat
from lantz.qt import Backend, Frontend, InstrumentSlot

class FLOWPIDDriver(INODriver):
        
    def __init__(self,Kp,Ki,Kd,Set_Point):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Set_Point = Set_Point
        
    control_loop=BoolFeat('CONTROL_LOOP')
    Kp=QuantityFeat('KP')
    Ki=QuantityFeat('KI')
    Kd=QuantityFeat('KD')
    set_point=QuantityFeat('SET_POINT', units='L')
    flow_value = QuantityFeat('FLOW_VALUE')
   
    open_valve_1 = BoolFeat('OPEN_VALVE_1')
    close_valve_1 = BoolFeat('CLOSE_VALVE_1')
    open_vavle_2 = BoolFeat('OPEN_VALVE_2')
    close_valve_2 = BoolFeat('CLOSE_VALVE_2')
 ''' Esto es para obtener el estado de la valvula. Esto esta incluido en las funciones de arriba? '''  
#    valve_1_status = BoolFeat()
#    valve_2_status = BoolFeat()

class FLOWPIDBackend(Backend):
    board: LEDPIDDriver = InstrumentSlot


''' Esta bien definido self.board.Kp=self.board.Kp?? ''' 
    def enable_control_loop_method(self):
        self.board.control_loop = True
    
    def disable_control_loop_method(self):
        self.board.control_loop = False
        
    def set_Kp(self):
        self.board.Kp = self.board.Kp
        
    def set_Ki(self):
        self.board.Kp = self.board.Ki
        
    def set_Kd(self):
        self.board.Kp = self.board.Kd
        
    def set_set_point(self):
        self.board.set_point = self.board.Set_Point
    
    def open_valve_1_method(self):
        self.board.open_valve_1 = True
   
    def close_valve_1_method(self):
        self.board.open_valve_1 = False

    def open_valve_2_method(self):
        self.board.open_valve_1 = True
        
    def close_valve_2_method(self):
        self.board.open_valve_1 = False
        
        
'''Revisar esto, y ver como hacer para darle un valor al flujo y que lo setee ahi '''      
    def get_flow(self):
        print(self.board.flow_value)
        
    def set_flow(self,Flow_Value):
        self.board.flow_value = self.board.flow
        
        

class FLOWPIDUserInterfase(Frontend):
    gui = 'LEDPID.ui'

    def connect_backend(self):
        super().connect_backend()
        self.widget.enable_control_loop_button.clicked.connect(self.backend.enable_control_loop_method)
        self.widget.disable_control_loop_button.clicked.connect(self.backend.disable_control_loop_method)
        self.widget.open_valve_1_button.clicked.connect(self.backend.open_valve_1_method)
        self.widget.close_valve_1_button.clicked.connect(self.backend.close_valve_1_method)
        self.widget.open_valve_2_button.clicked.connect(self.backend.open_valve_2_method)
        self.widget.close_valve_2_button.clicked.connect(self.backend.close_valve_2_method)



if __name__ == '__main__':
    from lantz.core.log import log_to_screen, log_to_socket, DEBUG
    from lantz.qt import start_gui_app, wrap_driver_cls
    
    # ~ log_to_socket(DEBUG) # Uncommment this line to log to socket
    log_to_screen(DEBUG) # or comment this line to stop logging

    QFLOWPID = wrap_driver_cls(FLOWPIDDriver)
    with QFLOWPID.via_packfile('FLOWPIDDriver.pack.yaml', check_update=True) as board:
        app = FLOWPIDBackend(board=board)
        start_gui_app(app, FLOWPIDUserInterfase)