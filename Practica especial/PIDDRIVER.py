# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:02:27 2019

@author: Publico
"""

import lantz.ino import INODriver, BoolFeat, QuantityFeat
from lantz.qt import Backend, Frontend, InstrumentSlot

class LEDPIDDriver(INODriver):
        
    def __init__(self,Kp,Ki,Kd,Set_Point):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Set_Point = Set_Point
        
    control_loop=BoolFeat('CONTROL_LOOP')
    
    Kp=QuantityFeat('KP')
    Ki=QuantityFeat('KI')
    Kd=QuantityFeat('KD')
    set_point=QuantityFeat('SET_POINT'units='L')
    
    
    
    @Feat()
    def flow_value(self):
        return self.kp_value
    
    @kp.setter
    def flow_value(self):
        self.write
    



class LEDPIDBackend(Backend):
    board: LEDPIDDriver = InstrumentSlot
    

    def enable_control_loop_method(self):
        self.board.control_loop = True
    
    def disable_control_loop_method(self):
        self.board.control_loop = False
        
    def get_flow(self):
        self.
        
    def set_flow(self,Flow_Value):
        self
        
        

class LEDPIDUserInterfase(Frontend):
    gui = 'LEDPID.ui'

    def connect_backend(self):
        super().connect_backend()
        self.widget.enable_control_loop_button.clicked.connect(self.backend.enable_control_loop_method)
        self.widget.disable_control_loop_button.clicked.connect(self.backend.disable_control_loop_method)



if __name__ == '__main__':
    from lantz.core.log import log_to_screen, log_to_socket, DEBUG
    from lantz.qt import start_gui_app, wrap_driver_cls
    
    # ~ log_to_socket(DEBUG) # Uncommment this line to log to socket
    log_to_screen(DEBUG) # or comment this line to stop logging

    QLEDPID = wrap_driver_cls(LEDPIDDriver)
    with QLEDPID.via_packfile('LEDPIDDriver.pack.yaml', check_update=True) as board:
        app = LEDPIDBackend(board=board)
        start_gui_app(app, LEDPIDUserInterfase)