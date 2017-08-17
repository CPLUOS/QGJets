#!/usr/bin/env python

import ROOT as r

f=r.TFile("analysis_LHE_QCD_HT500toInf.root")

c=r.TCanvas()
c.Divide(2,2)

c.cd(1)
f.jetAnalyser.Draw("dau_deta:dau_dphi >> h1(20,-0.4,0.4,20,-0.4,0.4)", "dau_pt*(dau_charge==0 && dau_ishadronic==1)", "colz", 15)
c.cd(2)
f.jetAnalyser.Draw("dau_deta:dau_dphi >> h2(20,-0.4,0.4,20,-0.4,0.4)", "dau_pt*(dau_charge==0 && dau_ishadronic==0)", "colz", 15)
c.cd(3)
f.jetAnalyser.Draw("dau_deta:dau_dphi >> h3(20,-0.4,0.4,20,-0.4,0.4)", "dau_pt*(abs(dau_charge)==1 && dau_ishadronic==0)", "colz", 15)

c.Print("test.png")

# ALL
h = r.TH1F("dr", ";#Delta R;# Jet Daughters", 100, 0.0, 0.2)
pi = r.TLorentzVector()
pj = r.TLorentzVector()
for i in range(100):
    _ = f.jetAnalyser.GetEntry(i)
    for i in range(f.jetAnalyser.dau_deta.size()):
        pi.SetPtEtaPhiM(f.jetAnalyser.dau_pt[i], f.jetAnalyser.dau_deta[i], f.jetAnalyser.dau_dphi[i], 0)
        for j in range(i+1, f.jetAnalyser.dau_deta.size()):
            pj.SetPtEtaPhiM(f.jetAnalyser.dau_pt[j], f.jetAnalyser.dau_deta[j], f.jetAnalyser.dau_dphi[j], 0)
            dR = pi.DeltaR(pj)
            _ = h.Fill(dR)

# Cf. Hadronic
h = r.TH1F("dr", ";#Delta R;# Jet Daughter Pairs", 100, 0.0, 0.2)
pi = r.TLorentzVector()
pj = r.TLorentzVector()
for i in range(100):
    _ = f.jetAnalyser.GetEntry(i)
    for i in range(f.jetAnalyser.dau_deta.size()):
        if not f.jetAnalyser.dau_ishadronic[i]: continue
        pi.SetPtEtaPhiM(f.jetAnalyser.dau_pt[i], f.jetAnalyser.dau_deta[i], f.jetAnalyser.dau_dphi[i], 0)
        for j in range(0, f.jetAnalyser.dau_deta.size()):
            if f.jetAnalyser.dau_ishadronic[j]: continue
            pj.SetPtEtaPhiM(f.jetAnalyser.dau_pt[j], f.jetAnalyser.dau_deta[j], f.jetAnalyser.dau_dphi[j], 0)
            dR = pi.DeltaR(pj)
            _ = h.Fill(dR)

