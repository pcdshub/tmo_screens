#! /bin/bash

# Setup edm environment

if [ -e /reg/g/pcds/pyps/config/common_dirs.sh ]; then
    source /reg/g/pcds/pyps/config/common_dirs.sh
else
    source /afs/slac/g/pcds/config/common_dirs.sh
fi

export HUTCH=tmo

# Setup edm environment
source $SETUP_SITE_TOP/epicsenv-cur.sh
pushd $EPICS_SITE_TOP-dev/screens/edm/${HUTCH}/current

edm -x -eolc \
    -m "LASR=TMO" \
    -m "FSNUM=14" \
    -m "P=LAS:FS14:VIT"	\
    -m "CH=LAS:FS14:VIT:CH1_"	\
    -m "IOC=LAS:FS14:IOC:VIT" \
    -m "EVR=EVR:LAS:LHN:04" \
    -m "EVR_IOC=IOC:LAS:LHN:EVR:04" \
    -m "FREQ_MOTOR=LAS:FS14:MMN:FQ" \
    -m "FREQ_MOTOR_IOC=LAS:FS14:IOC:MMS:FQ" \
    -m "PHASE_MOTOR=LAS:FS14:MMS:PH"	\
    -m "PHASE_MOTOR_IOC=LAS:FS14:IOC:MMS:PH"	\
    -m "SR620=LAS:FS14:CNT:TI"	\
    -m "SR620_IOC=LAS:FS14:IOC:CNT:TI" \
    -m "AG5322=LAS:FS14:CNT:FQ"	\
    -m "AG5322_IOC=LAS:FS14:IOC:CNT:FQ" \
    -m "IPM=EM2K0:XGMD:HPS:milliJoulesPerPulse" \
    vitaraScreens/emb-vitara-tt.edl &
