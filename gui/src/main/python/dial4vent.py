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

from PyQt5.QtWidgets import QWidget, QDial, QGridLayout, QLabel
from pyqtgraph.Qt    import QtGui, QtCore
from bar4vent        import _Bar

class dial_4vent(QWidget):
    style ='''
    QDial
    {
        background-color: rgb(255,255,255);
        font: 15px Menlo;
        color: rgb(0, 0, 131);
        /*text-align: left;*/
    }
    QLabel {
        /*border: 1px solid white;*/
        border-radius: 5px;
        background-color:  rgb(172, 236, 217);
        font: 15px Verdana, sans-serif;
        color:  rgb(0, 0, 131);
        text-align: center;
    }
    '''
    def __init__(self, title, min, max, **kwargs):
        super().__init__()
        self.title = title
        self.min   = min;self.max = max; self.moved_cbs = []
        self.layout = QGridLayout()
        self.label0 = QLabel(self)
        self.label  = QLabel(self)
        self.dial   = QDial()
        self.bar    = _Bar(["#5e4fa2", "#3288bd", "#66c2a5", "#abdda4",
                            "#e6f598", "#ffffbf", "#fee08b", "#fdae61",
                            "#f46d43", "#d53e4f", "#9e0142"])
        #_Bar(20) for pink ["#49006a", "#7a0177", "#ae017e", "#dd3497", "#f768a1", "#fa9fb5", "#fcc5c0", "#fde0dd", "#fff7f3"]
        self.label0.setStyleSheet(self.style)
        self.dial.setStyleSheet(self.style)
        self.label.setStyleSheet(self.style)
        self.dial.setMinimum(self.min)
        self.dial.setMaximum(self.max)
        self.dial.setValue(self.max)
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.slider_moved)
        self.dial.setWrapping(False)
        self.dial.setGeometry(QtCore.QRect(25,25,100,100))
        self.layout.addWidget(self.label0, 0, 0, 1, 1)
        self.layout.addWidget(self.dial,1,0,1,1)
        self.layout.addWidget(self.bar,1,1,1,1)
        self.layout.addWidget(self.label,2,0, 1, 1)
        self.setLayout(self.layout)
        self.label0.setText(self.title)
        self.label.setStyleSheet("font-family: Impact, Charcoal, sans-serif");
        self.label.setText(str(self.dial.value()))
        #self.dial.installEventFilter(self) ## disables person using mouse
        self.show()
        ## Bar related initalization
        self.add_slider_moved(self.bar._trigger_refresh)
        # Take NO feedback from click events on the meter.
        self.bar.installEventFilter(self)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self[name]
        return getattr(self.dial, name)

    def eventFilter(self, source, event):
        if (source is self.dial and isinstance(event, (
            QtGui.QMouseEvent, QtGui.QWheelEvent, QtGui.QKeyEvent))):
            return True
        return QtGui.QWidget.eventFilter(self, source, event)

    def slider_moved(self):
        self.label.setText(str(self.dial.value()))
        for fn in self.moved_cbs:
            fn()
    def add_slider_moved(self, func):
        self.moved_cbs.append(func)

    def setColor(self, color):
        self.bar.steps = [color] * self.bar.n_steps
        self.bar.update()

    def setColors(self, colors):
        self.bar.n_steps = len(colors)
        self.bar.steps = colors
        self.bar.update()

    def setBarPadding(self, i):
        self.bar._padding = int(i)
        self.bar.update()

    def setBarSolidPercent(self, f):
        self.bar.bar_solid_percent = float(f)
        self.bar.update()

    def setBackgroundColor(self, color):
        self.bar._background_color = QtGui.QColor(color)
        self.bar.update()
