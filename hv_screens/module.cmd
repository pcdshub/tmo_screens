#! /bin/bash

# Setup the common directory env variables
if [ -e /reg/g/pcds/pyps/config/common_dirs.sh ]; then
        source /reg/g/pcds/pyps/config/common_dirs.sh
else
        source /afs/slac/g/pcds/config/common_dirs.sh
fi

export IOC_PV=TMO:MPOD:01:IOC
export HUTCH=tmo

# Setup edm environment
source $SETUP_SITE_TOP/epicsenv-cur.sh
pushd /reg/g/pcds/epics-dev/spencera/tmo/screens/isegPower

# Launch edm
edm -x -eolc    \
        -m "DEV=TMO:MPOD:01"    \
        -m "IOC=TMO:MPOD:01:IOC"        \
        -m "HUTCH=tmo"  \
        -m "MOD0=TMO:MPOD:01"   \
        -m "MOD1=TMO:MPOD:01"   \
        -m "MOD2=TMO:MPOD:01"   \
        -m "MOD3=TMO:MPOD:01"   \
        -m "MOD4=TMO:MPOD:01"   \
        -m "MOD5=TMO:MPOD:01"   \
        -m "MOD6=TMO:MPOD:01"   \
        -m "MOD7=TMO:MPOD:01"   \
        -m "MOD8=TMO:MPOD:01"   \
        -m "MOD9=TMO:MPOD:01"   \
	-m "MOD=TMO:MPOD:01:M$1"	\
	isegPowerScreens/apalis16ChModule.edl &

