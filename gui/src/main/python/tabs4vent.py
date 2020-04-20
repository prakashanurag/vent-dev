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

from   PyQt5.QtWidgets import QPushButton, QMessageBox, QSizePolicy
from   utils           import *

class tab_4vent(QPushButton):
    def __init__(self, label, **kwargs):
        super().__init__()
        self.label = label; self.css = "background-color: rgb(160, 223, 219)"
        self.click = self._on_click
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "func":
                    self.click = value
                if key == "css":
                    self.css = value
        super().setText(self.label)
        super().clicked.connect(self.click)
        super().setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        super().setStyleSheet(self.css)
    def __str__(self):
        return '({0.label!s}, {0.click})'.format(self)
    def _on_click(self):
        super().setStyleSheet("background-color: rgb(0, 223, 219)")
        alert = QMessageBox()
        alert.setText('You clicked %s!' % self.label)
        alert.exec_()
        super().setStyleSheet(self.css)
    def tab_connect(self, func):
        self.click = func
        super().clicked.connect(self.click)
