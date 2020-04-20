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

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from pyqtgraph.Qt                          import QtGui, QtCore
from frontend                              import front_end
import constants
import pyqtgraph                           as     pg
import sys

pg.setConfigOption('background', pg.mkColor(186, 227, 230))
pg.setConfigOption('foreground', 'k')

app          = QtGui.QApplication(sys.argv)
main_dialog  = front_end('vent4us', width=1200, height=1080)
main_dialog.create_grid_layout()
main_dialog.animate(constants.__CADENCE__) # Change the cadence of plot updates here - its set to 200 ms = 0.2 second

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        exit_code = QtGui.QApplication.instance().exec_()
    sys.exit(exit_code)
