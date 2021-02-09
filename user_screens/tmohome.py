import os
from pydm import Display
import yaml
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner
from PyQt5.QtWidgets import QTableWidgetItem as qtw
from PyQt5 import QtCore, QtGui
from pydm.widgets import PyDMLabel

UI_FILE = 'tmohome.ui'

class TMOHome(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(TMOHome, self).__init__(parent=parent, args=args, macros=macros)
        self._connect_signals()

    def _connect_signals(self):
        pass

    def ui_filename(self):
        """Boiler plate pydm"""
        return UI_FILE

    def ui_filepath(self):
        """Boiler plate pydm"""
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, self.ui_filename())
