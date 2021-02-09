#!/bin/bash

#source /reg/g/pcds/pyps/conda/py36env.sh
source /reg/g/pcds/pyps/conda/dev_conda

typhos devices "pcdsdevices.epics_motor.SmarAct[{'prefix':'LM1K4:EJX_MP1_OAP1', 'name':'LM1K4:EJX_MP1_OAP1'}]" \
               "pcdsdevices.epics_motor.SmarActTipTilt[{'prefix':'LM1K4:EJX_MP1_OAP1', 'tip_pv':'_TIP1', 'tilt_pv':'_TILT1', 'name':'LM1K4:EJX_MP1_OAP1_MR1'}]" \
               "pcdsdevices.epics_motor.SmarActTipTilt[{'prefix':'LM1K4:EJX_MP1_OAP1', 'tip_pv':'_TIP3', 'tilt_pv':'_TILT3', 'name':'LM1K4:EJX_MP1_OAP1_MR3'}]" \
               "pcdsdevices.epics_motor.SmarAct[{'prefix':'LM1K4:INJ_MP1_ATT1_WP1', 'name':'LM1K4:INJ_MP1_ATT1_WP1'}]" \
               "pcdsdevices.epics_motor.SmarAct[{'prefix':'LM1K4:INJ_DP2_MR1', 'name':'LM1K4:INJ_DP2_MR2'}]" &
