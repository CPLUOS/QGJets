import os
import ROOT

def ensure(direc):
    if not os.path.exists(direc):
        os.system("mkdir -p "+direc)

ROOT.gStyle.SetOptStat(0)
#ROOT.gSystem.Load("../../install//Delphes-3.4.1/libDelphes")
ROOT.gSystem.Load(os.getenv("HOME")+"/install//delphes/libDelphes")
# Delphes doesn't output the structure information to the lib for some
# reason so need to include the header for ROOT to be able to read
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')

f=ROOT.TFile("../0-GenerateJets/delphes_PythiaZJets_CUETP8M1.root")
f.Delphes.GetEntry(0)
for i in range(len(f.Delphes.Particle)):
    particle = f.Delphes.Particle[i]
    print i, particle.PID, particle.Status, particle.M1, particle.M2, particle.D1, particle.D2, "<<<" if particle.Status == 23 else ""

f=ROOT.TFile("GenRoot/pp_zq_cuep8m1.root")
f.Delphes.GetEntry(1)
for i, p in enumerate(f.Delphes.Particle):
    force = False # p.M1 <= 7 <= (p.M2 if p.M2 >= 0 else p.M1)
    if (p.Status < 10 or p.Status > 40) and not force: continue
    if p.PT == 0 and not force: continue
    print i, p.PID, p.Status, p.PT, p.Eta, p.Phi, "...", p.M1, p.M2
