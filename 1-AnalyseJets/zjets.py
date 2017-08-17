import os
import ROOT

def ensure(direc):
    if not os.path.exists(direc):
        os.system("mkdir -p "+direc)

ROOT.gStyle.SetOptStat(0)
ROOT.gSystem.Load("../../install//Delphes-3.4.1/libDelphes.so")
# Delphes doesn't output the structure information to the lib for some
# reason so need to include the header for ROOT to be able to read
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')

f=ROOT.TFile("../0-GenerateJets/delphes_PythiaZJets_CUETP8M1.root")
f.Delphes.GetEntry(0)
for i in range(len(f.Delphes.Particle)):
    particle = f.Delphes.Particle[i]
    print i, particle.PID, particle.Status, particle.M1, particle.M2, particle.D1, particle.D2, "<<<" if particle.Status == 23 else ""

