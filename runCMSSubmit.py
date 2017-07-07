#!/usr/bin/env python2

import os
from glob import glob

files = glob('/xrootd/store/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/*/*root')
files = [f.replace('/xrootd', 'root://cms-xrdr.sdfarm.kr:1094///xrd')
         for f in files]
files = [files[n:n+10] for n in range(0,len(files),10)]

for filelist in files:
    os.system("""condor_submit runCMS.jds -append 'environment = "DELPHES_CMS_FILELIST=%s"'""" % ','.join(filelist))
