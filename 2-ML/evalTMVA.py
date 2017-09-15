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
reader.BookMVA('BDT', 'delphes/weights/TMVAClassification_BDT.weights.xml')

def runTMVA(tsig, tbkg, name='default', matching=True, useFlavor=False, balanced=False, passZJets=False):
    global c, arr, reader
    sig = ROOT.TH1F("sig", "sig", 50, -0.5, 0.5)
    bkg = ROOT.TH1F("bkg", "bkg", 50, -0.5, 0.5)
    mvaBDT = ROOT.vector('float')()
    mvaT = ROOT.vector('bool')()
    for jet in tsig:
#        if jet.pt < 50: continue
        if matching and not jet.matched: continue
        if balanced and not jet.balanced: continue
        if passZJets and not jet.pass_Zjets: continue
        arr[0][0] = jet.cmult
        arr[1][0] = jet.nmult
        arr[2][0] = jet.axis1
        arr[3][0] = jet.axis2
        arr[4][0] = jet.ptD
        arr[5][0] = jet.pt_dr_log
        mva = reader.EvaluateMVA('BDT')
        sig.Fill(mva)
        mvaT.push_back(1)
        mvaBDT.push_back(mva)
    for jet in tbkg:
#        if jet.pt < 50: continue
        if matching and not jet.matched: continue
        if balanced and not jet.balanced: continue
        if passZJets and not jet.pass_Zjets: continue
        arr[0][0] = jet.cmult
        arr[1][0] = jet.nmult
        arr[2][0] = jet.axis1
        arr[3][0] = jet.axis2
        arr[4][0] = jet.ptD
        arr[5][0] = jet.pt_dr_log
        mva = reader.EvaluateMVA('BDT')
        bkg.Fill(mva)
        mvaT.push_back(0)
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

# f = ROOT.TFile("AnalyseRoot/PythiaQCD_CUETP8M1_flat.root")
# runTMVA(f)

# f = ROOT.TFile("AnalyseRoot/PythiaQCD_Tune4C_flat.root")
# runTMVA(f, 'PythiaQCD_Tune4C_flat')

# f = ROOT.TFile("AnalyseRoot/PythiaZJets_Tune4C.root")
# runTMVA(f, 'PythiaZJets_Tune4C', matching=False, useFlavor=True)

fqq = ROOT.TFile("AnalyseRoot/pp_qq_cuep8m1.root")
# runTMVA(f, 'qq', matching=False, useFlavor=False, balanced=True)
fgg = ROOT.TFile("AnalyseRoot/pp_gg_cuep8m1.root")
runTMVA(fgg.jetAnalyser, fqq.jetAnalyser, 'qqgg', matching=False, useFlavor=False, balanced=True)

fzq = ROOT.TFile("AnalyseRoot/pp_zq_cuep8m1.root")
#runTMVA(f, 'zq', matching=False, useFlavor=False, passZJets=True)
fzg = ROOT.TFile("AnalyseRoot/pp_zg_cuep8m1.root")
runTMVA(fzg.jetAnalyser, fzq.jetAnalyser, 'zqg', matching=False, useFlavor=False, passZJets=True)
