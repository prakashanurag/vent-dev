# set QT_API environment variable
import os
os.environ["QT_API"] = "pyqt5"
import qtpy

# qt libraries
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from qtpy.QtGui import *

import ventapp.control.utils as utils
from ventapp.control._def import *

from queue import Queue
import time
import numpy as np
import pyqtgraph as pg
from datetime import datetime

class ValveController(QObject):

    xPos = Signal(float)
    yPos = Signal(float)

    def __init__(self,microcontroller):
        QObject.__init__(self)
        self.microcontroller = microcontroller
        self.x_pos = 0
        self.y_pos = 0

    def move_x(self,delta):
        self.microcontroller.move_x(delta)
        self.x_pos = self.x_pos + delta
        self.xPos.emit(self.x_pos)
        QApplication.processEvents()
        #print(self.x_pos)

    def move_y(self,delta):
        self.microcontroller.move_y(delta)
        self.y_pos = self.y_pos + delta
        self.yPos.emit(self.y_pos)
        QApplication.processEvents()

    def open_valve_1(self):
        self.microcontroller.toggle_valve_1(1)

    def open_valve_2(self):
        self.microcontroller.toggle_valve_2(1)

    def close_valve_1(self):
        self.microcontroller.toggle_valve_1(0)

    def close_valve_2(self):
        self.microcontroller.toggle_valve_2(0)

class Waveforms(QObject):

    signal_Paw = Signal(float,float)
    signal_Volume = Signal(float,float)
    signal_Flow = Signal(float,float)

    def __init__(self,microcontroller):
        QObject.__init__(self)
        self.microcontroller = microcontroller
        self.Paw = 0
        self.Volume = 0
        self.Flow = 0
        self.time = 0
        self.timer_update_waveform = QTimer()
        self.timer_update_waveform.setInterval(WAVEFORMS.UPDATE_INTERVAL_MS)
        self.timer_update_waveform.timeout.connect(self.update_waveforms)
        self.timer_update_waveform.start()

    def update_waveforms(self):
        self.time = self.time + (1/1000)*WAVEFORMS.UPDATE_INTERVAL_MS
        self.time = self.time%WAVEFORMS.DISPLAY_RANGE_S
        readout = self.microcontroller.read_received_packet_nowait()
        if readout is not None:
            self.Paw = (utils.unsigned_to_signed(readout[0:2],MicrocontrollerDef.N_BYTES_DATA)/(65536/2))*MicrocontrollerDef.PAW_FS
            self.Flow = (utils.unsigned_to_signed(readout[2:4],MicrocontrollerDef.N_BYTES_DATA)/(65536/2))*MicrocontrollerDef.FLOW_FS
            self.Volume = (utils.unsigned_to_unsigned(readout[4:6],MicrocontrollerDef.N_BYTES_DATA)/65536)*MicrocontrollerDef.VOLUME_FS

        self.signal_Paw.emit(self.time,self.Paw)
        self.signal_Flow.emit(self.time,self.Flow)
        self.signal_Volume.emit(self.time,self.Volume)



        # print(self.Paw)
        # print(self.Flow)
        # print(self.Volume)
        # print('----------')

        # self.Paw = (self.Paw + 0.01)%5
        # self.Volume = (self.Volume + 0.01)%5
        # self.Flow = (self.Flow + 0.01)%5
        # print(self.Paw)
