import ROOT

ROOT.gSystem.Load("../install//Delphes-3.4.1/libDelphes.so")
# Delphes doesn't output the structure information to the lib for some
# reason so need to include the header for ROOT to be able to read
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')

f = ROOT.TFile("delphes_QCD2000.root")
f.Delphes.GetEntry(0)
f.Delphes.Jet[0].Constituents[0]

#fa = ROOT.TFile("analysis_QCD2000.root")
#fa = ROOT.TFile("analysis_Pythia_HardQCD.root")
fa = ROOT.TFile("analysis_QCD_HT2000toInf.root")
#fa = ROOT.TFile("analysis_HT50.root")
# fa.jetAnalyser.Print()
fa.jetAnalyser.Draw("n_dau")

for ev in fa.jetAnalyser:
    ndch = 0
    ndne = 0
    for ch in ev.dau_charge:
        if ch == 0: ndne += 1
        else: ndch += 1
    if ndch != ev.cmult:
        print "CH", ev.cmult, ndch
    if ndne != ev.nmult:
        print "NE", ev.nmult, ndne

# Compare with Seungjins file
fslo = ROOT.TFile("/cms/scratch/slowmoyang/CMSSW_8_0_26/src/jetIdentification/jetAnalyser/test/jet.root")

var = ""
fslo.jetAnalyser.Get("jetAnalyser").Draw(var)
fa.jetAnalyser.Draw(var, "", "Same")

tslo = fslo.jetAnalyser.Get("jetAnalyser")
ta = fa.jetAnalyser

def nJets(name, tr):
    last = -1
    n = 0
    jets = ROOT.TH1F(name, ";n jets;events", 21, -0.5, 20.5)
    for ev in tr:
        if last != -1 and last != ev.nEvent:
            _ = jets.Fill(n)
            n = 0
            last = ev.nEvent
        elif last == -1:
            last = ev.nEvent
        n += 1
    jets.Fill(n)
    return jets

slo = nJets("slo", fslo.jetAnalyser.Get("jetAnalyser"))
ana = nJets("ana", fa.jetAnalyser)
