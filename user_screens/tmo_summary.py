import os
import sys
from pydm import Display
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner
from PyQt5 import QtCore, QtGui, QtWidgets
from pydm.widgets import PyDMLabel

UI_FILE = 'tmo_summary.ui'
STYLE_FILE = 'style.css'
#app = QtWidgets.QApplication(sys.argv)
#file = QtCore.QFile(':/dark.qss')
#file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
#stream = QtCore.QTextStream(file)
#app.setStyleSheet(stream.readAll())


class TMOSummary(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(TMOSummary, self).__init__(parent=parent, args=args, macros=macros)
        #self._connect_signals()

    def _connect_signals(self):
        with open(STYLE_FILE, 'r') as f:
            self.setStyleSheet(f.read())

    def ui_filename(self):
        """Boiler plate pydm"""
        return UI_FILE

    def ui_filepath(self):
        """Boiler plate pydm"""
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, self.ui_filename())
