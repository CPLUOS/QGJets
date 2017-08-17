#!/usr/bin/env python2

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f', dest='files', nargs='+', default=['file:/xrootd/store/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/0042F883-9DB6-E611-B1DB-FA163E9CBC86.root'])

args = parser.parse_args()

if os.getenv('DELPHES_CMS_FILELIST') is not None:
    print("DELPHES_CMS_FILELIST set, overwriting argument input")
    args.files = os.getenv('DELPHES_CMS_FILELIST').split(',')

os.system('/cms/scratch/iwatson/jetAnalysis/DelphesCMSFWLite /cms/scratch/iwatson/jetAnalysis/Cards/delphes_card_CMS_PileUp.tcl delphesCMS_test.root '+' '.join(args.files))

os.system('/cms/scratch/iwatson/jetAnalysis/analysis delphesCMS_test.root analysis_CMS.root')
