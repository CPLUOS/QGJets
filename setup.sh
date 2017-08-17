#!/bin/sh

alias cmsenv='eval `scramv1 runtime -sh`'

cd /cms/scratch/iwatson/CMSSW_8_0_26_patch1/src
eval `scramv1 runtime -sh`
cd - &> /dev/null

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/cms/scratch/iwatson/install/lib

export PYTHIA8DATA=
