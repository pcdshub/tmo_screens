import os
import sys
import yaml
from pydm import Display
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner
from PyQt5 import QtCore, QtGui, QtWidgets
from pydm.widgets import PyDMLabel
import logging
import numpy as np
from threading import Lock, get_ident

BASE = '/cds/group/pcds/epics-dev/aegger/tmo_screens/user_screens/'
UI_FILE = 'tmo_summary.ui'
STYLE_FILE = 'style.css'
ALARM_FILE = 'alarm_list.yml'

logger = logging.getLogger(__name__)

class TMOSummary(Display):
    _cb_lock = Lock()
    _signal = QtCore.pyqtSignal(str, bool)
    def __init__(self, parent=None, args=None, macros=None, alarms_file=ALARM_FILE):
        super(TMOSummary, self).__init__(parent=parent, args=args, macros=macros)
        self._alarm_config = self.load_alarms(f'{BASE}{alarms_file}')
        self._signal.connect(self.change_color)

    def ui_filename(self):
        """Boiler plate pydm"""
        return UI_FILE

    def ui_filepath(self):
        """Boiler plate pydm"""
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, self.ui_filename())

    def load_alarms(self, alarm_file):
        """A way of having user defined alarms as these can change
        for different experimemnts"""
        try:
            with open(alarm_file) as f:
                alarm_config = yaml.load(f, Loader=yaml.FullLoader)
            
            for k in alarm_config.keys():
                EpicsSignalRO(k).subscribe(self.compare_clbk)    
            return alarm_config
        except Exception as e:
            logger.warning(f'Unable to load alarm config: {e}')

    def change_color(self, name, alarm):
        """Call a change to style sheet from main thread"""
        with self._cb_lock:
            style_sheet = getattr(self.ui, name).styleSheet()
            if alarm and style_sheet == '':
                getattr(self.ui, name).setStyleSheet('color: red')
            elif not alarm and style_sheet == 'color: red':
                getattr(self.ui, name).setStyleSheet('')

    def compare_clbk(self, *args, **kwargs):
        pv = getattr(kwargs['obj'], 'name')
        cur_val = getattr(kwargs['obj'], 'value')

        if pv in self._alarm_config.keys():
            oper = self._alarm_config[pv]['oper']
            val = self._alarm_config[pv]['val']
            name = self._alarm_config[pv]['name']
            
            # Go through comparison cases, if we hit an alarm
            # send to main thread to check if we should change style sheet
            # Also, if we don't hit an alarm, but are red, we'll change it back
            if oper == 'less' and cur_val < val:
                self._signal.emit(name, True)
            elif oper == 'more' and cur_val > val:
                self._signal.emit(name, True)
            elif oper == 'equal' and cur_val != val:
                self._signal.emit(name, True)
            else: 
                self._signal.emit(name, False)
