import os
from pydm import Display
import yaml
from ophyd import EpicsSignal, EpicsSignalRO, PVPositioner
from PyQt5.QtWidgets import QTableWidgetItem as qtw
from PyQt5 import QtCore, QtGui
from pydm.widgets import PyDMLabel

CONFIG_PATH = '/cds/home/opr/tmoopr/bin/configs/'
VSET = ':VoltageSet'
VGET = ':VoltageMeasure'
RAMPING = ':isVoltageRamp'
REXT = ':VoltageRampSpeed'
HEADERS = [
    'LAMP Part',
    'Voltage Setting',
    'Voltage Rdbck',
    'Scale?',
    'PV Base'
]
MOD_BASE = 'TMO:PRO2:MPOD:01:M'

class Part:
    def __init__(self, part):
        # Let errors propagate
        self._name = part.get('name')
        self._vset = part.get('vset')
        self._base = part.get('base')
        self._scale = part.get('scale')
        self._ramping = EpicsSignalRO(f'{self._base}{RAMPING}')
        self._set_voltage = EpicsSignal(f'{self._base}{VSET}')

    @property
    def name(self):
        return self._name

    @property
    def vset(self):
        return self._vset

    @property
    def base(self):
        return self._base

    def set_voltage(self, zero=False):
        if zero:
            self._set_voltage.put(0)
        else:
            self._set_voltage.put(self.vset)

    @property
    def ramping(self):
        return self._ramping.get() 

# Easier formatting of table
class Config:
    _ramping = False
    def __init__(self, config, table, rr_le):
        self._parts_list = config.get('parts')
        self._ramp_rate = config.get('ramp_rate', 1.0)
        self._table = table
        self._rr_le = rr_le
    
    @property
    def config(self):
        return {'ramp_rate': self.ramp_rate, 'parts': self._parts_list}

    @property
    def rows(self):
        return len(self._parts_list)

    @property
    def ramp_rate(self):
        return self._ramp_rate

    @ramp_rate.setter
    def ramp_rate(self, rate):
        try:
            self._ramp_rate = float(rate)
        except Exception as e:
            print(f'Unable to set ramp rate: {e}')

    @property
    def cols(self):
        """Columns for table, extra slot for readback"""
        return len(self._parts_list[0]) + 1

    @property
    def names(self):
        return [part['name'] for part in self._parts_list]

    @property
    def parts_list(self):
        return self._parts_list

    @property
    def parts(self):
        return [Part(part) for part in self._parts_list]

    def update_config(self):
        # Table being qtablewidget
        # Do schema checking here
        parts_list = []
        for row in range(self._table.rowCount()):
            name = self._table.item(row, 0).text()
            vset = int(self._table.item(row, 1).text())
            scale = bool(self._table.item(row, 3).checkState())
            base = self._table.item(row, 4).text()
            part = {'name': name, 'vset': vset, 'scale': scale, 'base': base}
            parts_list.append(part)

        self._parts_list = parts_list

    def save_config(self, file_name):
        self.update_config()
        with open(f'{CONFIG_PATH}{file_name}', 'w') as f:
            doc = yaml.dump(self.config, f)

    def populate_table(self):
        self._rr_le.setText(str(self.ramp_rate))
        self._table.setRowCount(self.rows)
        self._table.setColumnCount(self.cols)  # Name, voltage, pv base
        # Hardcode for now
        for row, part in enumerate(self.parts_list):
            name = part['name']
            voltage = part['vset']
            scale = part['scale']
            base = part['base']
            self._table.setItem(row, 0, qtw(name))
            self._table.setItem(row, 1, qtw(str(voltage)))
            self._table.setCellWidget(row, 2, self._create_label(base))
            self._table.setItem(row, 3, self._create_box(scale))
            self._table.setItem(row, 4, qtw(base))
        self._table.setHorizontalHeaderLabels(HEADERS)

    def _create_label(self, base):
        label = PyDMLabel()
        label.channel = f'ca://{base}{VGET}'
        label.precisionFromPV = False
        label.precision = 0

        return label

    def _create_box(self, checked):
        box = qtw()
        box.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        if checked:
            box.setCheckState(QtCore.Qt.Checked)
        else:
            box.setCheckState(QtCore.Qt.Unchecked)

        return box

    def set_voltages(self, zero=False):
        self.update_config()
        for part in self.parts:
            part.set_voltage(zero)

    def scale_vset(self, multiplier=1.0):
        if multiplier == 0:
            print('Turn voltages off instead of scaling by 0')
            return
        for row, part in enumerate(self.parts_list):
            scale = part['scale']
            if scale:
                new_voltage = int(part['vset'] * multiplier)
                self._table.setItem(row, 1, qtw(str(new_voltage)))
        self.update_config() 

class VMIRamper(Display):
    _config = None
    _mod_rr_pvs = [EpicsSignal(f'{MOD_BASE}{i}{REXT}') for i in range(8)]
    def __init__(self, parent=None, args=None, macros=None):
        super(VMIRamper, self).__init__(parent=parent, args=args, macros=macros)
        self._connect_signals()

    def _connect_signals(self):
        self.update_config_list()
        self.ui.config_load_btn.clicked.connect(self.load_config)
        self.ui.save_config_btn.clicked.connect(self.save_config)
        self.ui.ramp_rate_le.editingFinished.connect(self.update_rr)
        self.ui.set_scale_btn.clicked.connect(self.scale_voltage)
        self.ui.ramp_bn.clicked.connect(self.ramp_voltages)
        self.ui.ramp_0_bn.clicked.connect(self.ramp_0)

    @property
    def config(self):
        return self._config

    def ui_filename(self):
        """Boiler plate pydm"""
        return 'vmi_ramper.ui'

    def ui_filepath(self):
        """Boiler plate pydm"""
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())

    def update_config_list(self):
        """Update the configuration combo box file list"""
        self.ui.config_select_cb.clear()
        self.ui.config_select_cb.addItems(os.listdir(CONFIG_PATH))

    def ramp_0(self):
        if self.config:
            self.config.set_voltages(zero=True)

    def ramp_voltages(self):
        if self.config:
            self.config.set_voltages()

    def update_rr(self):
        """Process edits to ramp rate line edit"""
        for mod in self._mod_rr_pvs:
            mod.put(self.ui.ramp_rate_le.text())
        if self.config:
            self.config.ramp_rate = self.ui.ramp_rate_le.text()

    def scale_voltage(self):
        """Process edits to voltage scaling line edit"""
        if self.config:
            mutliplier = float(self.ui.scale_voltage_le.text())
            self.config.scale_vset(mutliplier)

    def load_config(self):
        """Load the config data from yaml file"""
        with open(f'{CONFIG_PATH}{self.ui.config_select_cb.currentText()}') as f:
            #try:
            yaml_config = yaml.load(f, Loader=yaml.FullLoader)
            self._config = Config(yaml_config, self.ui.device_table, self.ui.ramp_rate_le)
            self._config.populate_table()
            self.save_config_btn.setEnabled(True)
            #except Exception as e:
            #    print(f'Configuration file {f} is malformed')

    def save_config(self):
        """Saves the config"""
        new_config_name = self.ui.config_save_le.text()
        self._config.save_config(new_config_name)
        self.update_config_list()
