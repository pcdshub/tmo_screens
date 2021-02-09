import os
from pydm import Display
from epics import caput
import yaml
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner
from PyQt5.QtWidgets import QTableWidgetItem as qtw
from PyQt5 import QtCore, QtGui
from pydm.widgets import PyDMLabel

# Define Number of Modules
MODULES = 8

# Define Base for MPOD
MOD_BASE = 'TMO:PRO2:MPOD:01'

class MPODCrate(Display):
    _mods = [f'{MOD_BASE}:M{i}' for i in range(MODULES)]
    def __init__(self, parent=None, args=None, macros=None):
        super(MPODCrate, self).__init__(parent=parent, args=args, macros=macros)
        self.ui.crate_base_label.setText(MOD_BASE)
        self.ui.all_off_btn.clicked.connect(self.all_off)
        self.ui.all_on_btn.clicked.connect(self.all_on)

    def ui_filename(self):
        """Boiler plate pydm"""
        return 'mpod_crate.ui'

    def ui_filepath(self):
        """Boiler plate pydm"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())

    def all_off(self):
        caput(f'{MOD_BASE}:Crate:GlobalOnOff', 0)

    def all_on(self):
        for mod in self._mods:
            caput(f'{mod}:Control:doClear', 1)
        caput(f'{MOD_BASE}:Crate:GlobalOnOff', 1)
