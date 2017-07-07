#!/bin/bash

RESULT_DIR="RESULT"
DIR=`date +%Y%m%d%k%M`

/bin/mkdir -p $RESULT_DIR/$DIR
/bin/mkdir -p $RESULT_DIR/root

echo "Hello condor" >> $RESULT_DIR/$DIR/`hostname`.txt
echo "Working in" `pwd` >> $RESULT_DIR/$DIR/`hostname`.txt
echo "ls /"
ls /
echo "-"
echo `date` >> $RESULT_DIR/$DIR/`hostname`.txt
source /cvmfs/cms.cern.ch/cmsset_default.sh >> $RESULT_DIR/$DIR/`hostname`.txt
source /cms/scratch/iwatson/jetAnalysis/setup.sh >> $RESULT_DIR/$DIR/`hostname`.txt
python /cms/scratch/iwatson/jetAnalysis/generateDelphesSample.py
echo `date` >> $RESULT_DIR/$DIR/`hostname`.txt
echo "Done." >> $RESULT_DIR/$DIR/`hostname`.txt
