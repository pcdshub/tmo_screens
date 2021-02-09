#! /bin/bash

# Setup edm environment
source /reg/g/pcds/setup/epicsenv-3.14.12.sh
export EDMDATAFILES=".:.."

pushd /cds/group/pcds/epics-dev/screens/edm/tmo
edm -x -m "PRE=TMO:PWR:PRT:02,IOC=IOC:TMO:PWR:PRT:02" -eolc TrippLite_2.edl &
