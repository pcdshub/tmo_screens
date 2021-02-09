import os
from pydm import Display
import yaml
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner

PV = 

class TMOHutchVac(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(TMOHutchVac, self).__init__(parent=parent, args=args, macros=macros)
        print('yeah we launched python')
        self.ui.test_btn.clicked.connect(self.launch_endstation)

    def ui_filename(self):
        """Boiler plate pydm"""
        return 'tmoHutchVac.ui'

    def ui_filepath(self):
        """Boiler plate pydm"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())

    def launch_endstation(self):
        pass
