#!/usr/bin/env python

import ROOT
from array import array

c = ROOT.TCanvas()

arr = [array('f', [0.]) for _ in range(6)]
reader = ROOT.TMVA.Reader()
reader.AddVariable('cmult', arr[0])
reader.AddVariable('nmult', arr[1])
reader.AddVariable('axis1', arr[2])
reader.AddVariable('axis2', arr[3])
reader.AddVariable('ptD', arr[4])
reader.AddVariable('pt_dr_log', arr[5])
reader.BookMVA('BDT', 'weights/TMVAClassification_BDT.weights.xml')

def runTMVA(f, name='default', matching=True, useFlavor=False):
    global c, arr, reader
    sig = ROOT.TH1F("sig", "sig", 50, -0.5, 0.5)
    bkg = ROOT.TH1F("bkg", "bkg", 50, -0.5, 0.5)
    mvaBDT = ROOT.vector('float')()
    mvaT = ROOT.vector('bool')()
    for jet in f.jetAnalyser:
        if jet.pt < 100: continue
        if matching:
            if not jet.matched:
                continue
        arr[0][0] = jet.cmult
        arr[1][0] = jet.nmult
        arr[2][0] = jet.axis1
        arr[3][0] = jet.axis2
        arr[4][0] = jet.ptD
        arr[5][0] = jet.pt_dr_log
        mva = reader.EvaluateMVA('BDT')
        if useFlavor:
            if jet.flavorId == 21:
                mvaT.push_back(jet.flavorId == 21)
                _ = bkg.Fill(mva)
            else:
                mvaT.push_back(jet.flavorId == 21)
                _ = sig.Fill(mva)
        else:
            if jet.partonId == 21:
                mvaT.push_back(jet.partonId == 21)
                _ = bkg.Fill(mva)
            else:
                mvaT.push_back(jet.partonId == 21)
                _ = sig.Fill(mva)
        mvaBDT.push_back(mva)
    #
    print "Sig:", sig.GetEntries(), "Bkg:", bkg.GetEntries()
    ROOT.gROOT.ProcessLine(".L ROCCurve.C+")
    roc = ROOT.TMVA.ROCCurve(mvaBDT, mvaT)
    auc = roc.GetROCIntegral()
    print "AUC:", auc
    #
    bkg.SetLineColor(ROOT.kRed)
    sig.SetLineColor(ROOT.kGreen)
    bkg.SetMaximum(max(bkg.GetMaximum(), sig.GetMaximum()))
    bkg.Draw()
    sig.Draw("Same")
    c.Print("figures/"+name+".pdf")
    roc.GetROCCurve().Draw("AL")
    c.Print("figures/roc_"+name+".pdf")

f = ROOT.TFile("AnalyseRoot/PythiaQCD_CUETP8M1_flat.root")
runTMVA(f)

f = ROOT.TFile("AnalyseRoot/PythiaQCD_Tune4C_flat.root")
runTMVA(f, 'PythiaQCD_Tune4C_flat')

f = ROOT.TFile("AnalyseRoot/PythiaZJets_Tune4C.root")
runTMVA(f, 'PythiaZJets_Tune4C', matching=False, useFlavor=True)
