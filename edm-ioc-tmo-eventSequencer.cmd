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
    -m "HID=1,ID=1,IOC=TMO:ECS:IOC:01,ECS=ECS:SYS0,EVG=EVNT:SYS0" \
    eventSeqScreens/event_sequencer_gui.edl &
