import os
from pydm import Display
import yaml
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner
from PyQt5.QtWidgets import QTableWidgetItem as qtw
from PyQt5 import QtCore, QtGui
from pydm.widgets import PyDMLabel

ABORT_REQ_PV = 'TMO:USER:BYKIKS:ABORT'
CUR_EN_PV = 'IOC:IN20:EV01:BYKIKS_ABTACT'
CUR_SHOTS_PV = 'IOC:IN20:EV01:BYKIKS_ABTPRD'
LAST_EN_PV = 'TMO:USER:BYKIKS:ABORT_EN'
LAST_SHOTS_PV = 'TMO:USER:BYKIKS:LAST_NUM_SHOTS'

class BYKIKS_BURST(Display):
    _abort_req = EpicsSignal(ABORT_REQ_PV)
    _last_shots = EpicsSignalRO(LAST_SHOTS_PV)
    _last_enable = EpicsSignalRO(LAST_EN_PV)
    _cur_shots = EpicsSignal(CUR_SHOTS_PV)
    _cur_enable = EpicsSignal(CUR_EN_PV)
    def __init__(self, parent=None, args=None, macros=None):
        super(BYKIKS_BURST, self).__init__(parent=parent, args=args, macros=macros)
        self._abort_req.subscribe(self.abort_clbk)
        self.ui.clear_abort_btn.clicked.connect(self.clear_abort)

    def ui_filename(self):
        """Boiler plate pydm"""
        return 'bykiks_burst.ui'

    def ui_filepath(self):
        """Boiler plate pydm"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())

    def _set_emer_vis(self, val):
        """Hide or Show label if abort is active"""
        if int(val) is 1:
            #self.ui.abort_en_cb.setDisabled(True)
            #self.ui.num_shots_le.setDisabled(True)
            self.ui.emer_label.show()
            self.ui.clear_abort_btn.show()
        else:
            #self.ui.abort_en_cb.setDisabled(False)
            #self.ui.num_shots_le.setDisabled(False)
            self.ui.emer_label.hide()
            self.ui.clear_abort_btn.hide()

    def abort_clbk(self, value, **kwargs):
        self._set_emer_vis(value)

    def clear_abort(self):
        # Get the previous values and restore
        self._cur_shots.put(self._last_shots.get())
        self._cur_enable.put(self._last_enable.get())
        self._abort_req.put(0)
