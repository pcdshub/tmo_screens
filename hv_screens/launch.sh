#!/bin/bash

source /cds/group/pcds/pyps/conda/dev_conda
pushd /cds/group/pcds/epics-dev/screens/pydm/tmo_screens/hv_screens
pydm tmo_hv.py
popd
