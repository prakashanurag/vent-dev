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

from   PyQt5.QtWidgets    import QGroupBox, QDialog, QGridLayout
from   pyqtgraph.Qt       import QtGui, QtCore

from   label4vent      import label_4vent
from   tabs4vent       import tab_4vent
from   plot4vent       import plot_4vent
from   dial4vent       import dial_4vent
from   utils           import *
from   backend         import *
import constants, backend

class front_end(QDialog, QtGui.QMainWindow):
    def __init__(self, title, **kwargs):
        super().__init__()
        self.title  = title
        ''' The following arrays look weird for now and unnecessary code
            TODO: These need to be encapsulated into separate structure
        '''
        self.plots  = []
        self.labels = []
        self.bars   = []
        self.alms   = []
        self.left   = 10
        self.top    = 10
        self.width  = 1080
        self.height = 1020
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "width":
                    self.width = value
                if key == "height":
                    self.height = value
                if key == "left":
                    self.left = value
                if key == "top":
                    self.top = value
        super().setStyleSheet(open(css_file()).read())
        self.init_ui()

    def create_alarms(self, alarms=2):
        ''' Add top alarm bars here: sub-layout '''
        alarm_layout = QGridLayout()
        self.alarm_grp_box = QGroupBox()
        self.alarm_grp_box.setStyleSheet("background-color: rgb(106, 90, 205)");
        for r in range(len(constants.__MODES__)):
            alm = tab_4vent(constants.__MODES__[r], css="background-color: rgb(106, 90, 205); color: rgb(255,255,255);")
            #alarm_layout.setHorizontalSpacing(20)
            alarm_layout.addWidget(alm,0,r)
            self.alms.append(alm)
        self.alarm_grp_box.setLayout(alarm_layout)

    def create_plots(self, plots=3):
        plot_layout = QGridLayout()
        self.plot_grp_box = QGroupBox()
        r = 0
        for dict_item in constants.__PLOTS__:
            r = r+1
            plot = plot_4vent(dict_item['name'], dict_item['xrange'], dict_item['yrange'], size=constants.__SIZE__)
            plot.add_series(dict_item['name'], dict_item['callback'])
            #plot_layout.setVerticalSpacing(20)
            #plot_layout.setOriginCorner(50)
            plot_layout.addWidget(plot.get(),r+self.row_idx,0)
            self.plots.append(plot)
        self.plot_grp_box.setLayout(plot_layout)

    def create_labels(self, labels=5):
        label_layout = QGridLayout()
        self.label_grp_box = QGroupBox()
        for r in range(labels):
            label = label_4vent(constants.__RT_VALUES__[r])
            #label_layout.setVerticalSpacing(20)
            label_layout.addWidget(label,r+self.row_idx,1) # width and height derived from main dialog width and height
            self.labels.append(label)
        self.label_grp_box.setLayout(label_layout)

    def create_buttons(self, buttons=9):
        button_layout = QGridLayout()
        self.button_grp_box = QGroupBox()
        self.button_grp_box.setStyleSheet("background-color: rgb(172, 236, 217)");
        for r in range(len(constants.__CONFIG_VALUES__)):
            #button_layout.setVerticalSpacing(20)
            button_layout.addWidget(tab_4vent(constants.__CONFIG_VALUES__[r]),r+self.row_idx,2)
        self.button_grp_box.setLayout(button_layout)

    def create_bars(self, bars=7):
        bar_layout = QGridLayout()
        self.bar_grp_box = QGroupBox()
        self.bar_grp_box.setStyleSheet("background-color: rgb(172, 236, 217)");
        for r in range(len(constants.__DIAL_VALUES__)):
            bar = dial_4vent(constants.__DIAL_VALUES__[r], 0, 250)
            #bar_layout.setHorizontalSpacing(10)
            bar_layout.addWidget(bar,4+self.row_idx,r)
            self.bars.append(bar)
        self.bar_grp_box.setLayout(bar_layout)

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.create_grid_layout()
        window_layout = QGridLayout()
        ''' TODO: Grid layout seems a bit odd here with these numbers, but basically
                  we scale the plots to 4 times the size
        '''
        window_layout.addWidget(self.alarm_grp_box,0,0,1,-1)
        window_layout.addWidget(self.alarm_grp_box,0,0,1,-1)
        window_layout.addWidget(self.plot_grp_box,1,0,3,5)
        window_layout.addWidget(self.label_grp_box,1,5,3,1)
        window_layout.addWidget(self.bar_grp_box,4,0,1,7)
        window_layout.addWidget(self.button_grp_box,1,6,-1,1)
        self.setLayout(window_layout)

    def create_grid_layout(self, plots=3, buttons=9, labels=5, bars=7, alarms=2):
        ''' Need to convert to a dictionary of {title, {position:x,y}}'''
        self.row_idx = 0 # Keeps track of rows as we add widgets
        ''' Add alarms here: sub-layout '''
        self.create_alarms(alarms)
        self.row_idx = self.row_idx + 1
        ''' Add plots here: sub-layout '''
        self.create_plots(plots)
        ''' Add runtime-labels here: sub-layout'''
        self.create_labels(labels)
        ''' Add buttons here: sub-layout '''
        self.create_buttons(buttons)
        ''' Add bottom bars here: sub-layout '''
        self.create_bars(bars)

    def plot_values(self):
        ## Start a timer to rapidly update the plot in pw
        #print ("plot_values")
        for p in self.plots:
            p.run_series(constants.__SIZE__) # TODO Make sure the plots are of same size for now
        ''' TODO Convert to a multi threaded application for these processing
            Not only for the plots but also for the labels
        '''
        for l in self.labels:
            l.run_tmo_callbacks()

    def animate(self, time=50):
        self.show()
        self.tmr = QtCore.QTimer(self)
        self.tmr.timeout.connect(self.plot_values)
        self.tmr.start(time)
