import os
import sys
import yaml
import uuid
import json
from pydm import Display
from PyQt5 import QtCore, QtGui, QtWidgets
import logging
from pydm.widgets.embedded_display import PyDMEmbeddedDisplay as pemd

logger = logging.getLogger(__name__)
UI_FILE = 'screen_launcher.ui'
MOTOR_FILE = 'motor_OneLine.ui'

class DeviceScreen(Display):
    _displays = {}
    def __init__(self, parent=None, args=None, macros=None):
        super(DeviceScreen, self).__init__(parent=parent, args=args, macros=macros)
        self._connect_signals()
         #test = pemd(parent=self)
        #self.ui.main_layout.addWidget(test)

    @property
    def displays(self):
        return self._displays

    @displays.setter
    def displays(self, displays):
        if not isinstance(displays, dict):
            logger.warning('trying to set displays as not dictionary')
            return

        self._displays = displays

    def ui_filename(self):
        """Boiler plate pydm"""
        return UI_FILE

    def ui_filepath(self):
        """Boiler plate pydm"""
        cur_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(cur_path, self.ui_filename())

    def _connect_signals(self):
        """boilder plate connect signals"""
        self.ui.add_btn.clicked.connect(self._gen_emb_disp)

    def _gen_emb_disp(self):
        """Code to run to add embedded display"""
        #if not prefix:
        #    logger.warning('You have not specified a device prefix')
        #    return

        try:
            unique_id = uuid.uuid1()
            self._displays[unique_id] = prefix
        except Exception as e:
            logger.warning(f'Issue setting device screen: {e}')

        disp = pemd(parent=self)
        disp.macros = json.dumps({'MOTOR': 'TMO:VLS:MMS:FM'})
        disp.filename = MOTOR_FILE

        self.ui.main_layout.addWidget(disp)
