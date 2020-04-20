# coding=utf-8

# vent4us 15/04/20
# The MIT License (MIT)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from   PyQt5.QtCore    import Qt
from   PyQt5.QtWidgets import QSizePolicy, QLabel, QFrame
from   utils           import *
import pyqtgraph       as pg
import numpy           as np # Later for on connect functions - TBD ?
import os

class label_4vent(QLabel):
    def __init__(self, label, **kwargs):
        super().__init__()
        self.label = label
        self.value = ''
        self.thresh= 220
        self.series = []
        self._init_ui()
    def __str__(self):
        return '({0.label!s}'.format(self)

    def _init_ui(self):
        super().setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        super().setFrameStyle(QFrame.Panel | QFrame.Sunken)
        super().setText(self.value)
        super().setAlignment(Qt.AlignTop | Qt.AlignCenter)
        _def_dict = { 'name': 'default', 'func': self.tmo_call_back}
        self.series.append(_def_dict)
        super().setText(self.label)

    def tmo_call_back(self):
        ''' Note: the functions need to be globals and included in this file via backend.py'''
        x = np.random.random()*self.thresh
        alarm = False
        value = truncate(x, 2)
        if x < (self.thresh*0.01):
            alarm = True
        return value , alarm

    def add_tmo_callback(self, name, func):
        ''' Note: the functions need to be globals and included in this file via backend.py
                  for now overwrite the tmo callback function
        '''
        for dict_item in self.series:
            for key in dict_item:
                  if  key == 'name' and name == dict_item['name']:
                      dict_item['func'] = func
                      return
        self.series.append({ 'name': name, 'func': func})

    def run_tmo_callbacks(self):
        ''' Note: the functions need to be globals and included in this file via backend.py'''
        #self.add_tmo_callback('test1', self.tmo_call_back)
        self.value = ''
        for dict_item in self.series:
            value, alarm = dict_item['func']()
            if value and self.value is not '':
                self.value = self.value + ' , ' + value
            else:
                self.value = value
            if alarm:
                super().setStyleSheet("background-color: rgb(204, 153, 255)")
            else:
                super().setStyleSheet("background-color: rgb(186, 227, 230)")
        #super().setStyleSheet("font: "+str(15/len(self.series))+"px Menlo, sans-serif")
        if self.value is not '':
            super().setText('<p style="color:black;font-size:12px;font-family:Menlo;text-align:left">'+self.label+'</p>'+ '\n' +
                            '<p style="color:rgb(0,0,131);font-size:60px;font-family:Impact, Charcoal, sans-serif;text-align:left">'+self.value+'</p>')
        else:
            super().setText(self.label)
