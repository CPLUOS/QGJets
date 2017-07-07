#!/bin/bash

RESULT_DIR="RESULT"
DIR=`date +%Y%m%d%k%M`
RNDMDIR=`mktemp -d -t --tmpdir= output-XXXXXXXXXXXXXX`
OUTPUTDIR=$RESULT_DIR/$DIR/$RNDMDIR

/bin/mkdir -p $OUTPUTDIR

echo "Hello condor" >> $OUTPUTDIR/`hostname`.txt
echo "Working in" `pwd` >> $OUTPUTDIR/`hostname`.txt
echo "ls /"
ls /
echo "-"
echo `date` >> $OUTPUTDIR/`hostname`.txt
source /cvmfs/cms.cern.ch/cmsset_default.sh >> $OUTPUTDIR/`hostname`.txt
source /cms/scratch/iwatson/jetAnalysis/setup.sh >> $OUTPUTDIR/`hostname`.txt
export LD_LIBRARY_PATH=:/cms/scratch/iwatson/install/Delphes-3.4.1/:$LD_LIBRARY_PATH
cp /cms/scratch/iwatson/jetAnalysis/*pcm .
python /cms/scratch/iwatson/jetAnalysis/delphesCMS.py --files root://cms-xrdr.sdfarm.kr:1094///xrd/store/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0042F883-9DB6-E611-B1DB-FA163E9CBC86.root
mv analysis_CMS.root $OUTPUTDIR/
echo `date` >> $OUTPUTDIR/`hostname`.txt
echo "Done." >> $OUTPUTDIR/`hostname`.txt
