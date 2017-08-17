#!/usr/bin/env python

import ROOT as r
import os

r.gStyle.SetOptStat(0)

def ensure(direc):
    if not os.path.exists(direc):
        os.system("mkdir -p "+direc)

def getPlots(title=None):
    hg = r.gROOT.FindObject("hg")
    hq = r.gROOT.FindObject("hq")
    hg.SetLineColor(r.kRed)
    hq.SetLineColor(r.kBlue)
    if title is not None:
        hg.SetTitle(title)
        hq.SetTitle(title)
    return hg, hq

def plots(t, direc, cut='abs(eta) < 2.4', limit=None):
    if limit is None: limit = t.GetEntries()

    cut = "1.0/"+str(limit)+"*("+cut+")"
    
    r.gROOT.SetBatch(True)
    c = r.TCanvas()
    
    ensure(direc)
    t.Draw("partonId")
    c.Print(direc+"/partonId.pdf")

    t.Draw("ptD >> hg(,0,1)", cut + " * (partonId==21)", "", limit)
    t.Draw("ptD >> hq(,0,1)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";ptD;# Jets")
    hg.Draw("")
    hq.Draw("same")
    c.Print(direc+"/ptD.pdf")

    
    t.Draw("pt >> hg(,0,2000)", cut + " * (partonId==21)", "", limit)
    t.Draw("pt >> hq(,0,2000)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";p_{T} [GeV];# Jets")
    hg.Draw("")
    hq.Draw("same")
    c.Print(direc+"/pt.pdf")
    t.Draw("eta >> hg(,-2.5, 2.5)", cut + " * (partonId==21)", "", limit)
    t.Draw("eta >> hq(,-2.5, 2.5)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";#eta;# Jets")
    hg.Draw("")
    hq.Draw("same")
    c.Print(direc+"/eta.pdf")
    try:
        t.Draw("phi >> hg(,-3.2,3.2)", cut + " * (partonId==21)", "", limit)
        t.Draw("phi >> hq(,-3.2,3.2)", cut + " * (partonId!=21)", "", limit)
        hg, hq = getPlots(";#phi;# Jets")
        hg.Draw("")
        hq.Draw("same")
        c.Print(direc+"/phi.pdf")
    except:
        print("Couldn't do phi")
        pass

    t.Draw("pt_dr_log >> hg(,0,500)", cut + " * (partonId==21)", "", limit)
    t.Draw("pt_dr_log >> hq(,0,500)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";pt_dr_log;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/pt_dr_log.pdf")

    t.Draw("axis1 >> hg(,0,8)", cut + " * (partonId==21)", "", limit)
    t.Draw("axis1 >> hq(,0,8)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";axis1;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/axis1.pdf")

    t.Draw("axis2 >> hg(,0,9)", cut + " * (partonId==21)", "", limit)
    t.Draw("axis2 >> hq(,0,9)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";axis2;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/axis2.pdf")

    t.Draw("nmult >> hg(,0,65)", cut + " * (partonId==21)", "", limit)
    t.Draw("nmult >> hq(,0,65)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";nmult;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/nmult.pdf")

    t.Draw("cmult >> hg(,0,65)", cut + " * (partonId==21)", "", limit)
    t.Draw("cmult >> hq(,0,65)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";cmult;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/cmult.pdf")

    try:
        t.Draw("leading_dau_pt >> hg(,0,1000)", cut + " * (partonId==21)", "", limit)
        t.Draw("leading_dau_pt >> hq(,0,1000)", cut + " * (partonId!=21)", "", limit)
        hg, hq = getPlots(";leading daughter p_{T} [GeV];# Jets")
        hg.Draw("hist")
        hq.Draw("hist same")
        c.Print(direc+"/leading_dau_pt.pdf")

        t.Draw("leading_dau_eta >> hg(,-0.5,0.5)", cut + " * (partonId==21)", "", limit)
        t.Draw("leading_dau_eta >> hq(,-0.5,0.5)", cut + " * (partonId!=21)", "", limit)
        hg, hq = getPlots(";leading daughter #Delta#eta;# Jets")
        hq.Draw("")
        hg.Draw("same")
        c.Print(direc+"/leading_dau_deta.pdf")
    except:
        pass

    t.Draw("dau_pt[0] >> hg(,0,1000)", cut + " * (partonId==21)", "", limit)
    t.Draw("dau_pt[0] >> hq(,0,1000)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";leading daughter p_{T} [GeV];# Jets")
    hg.Draw("hist")
    hq.Draw("hist same")
    c.Print(direc+"/first_dau_pt.pdf")
    
    t.Draw("dau_deta[0] >> hg(,-0.5,0.5)", cut + " * (partonId==21)", "", limit)
    t.Draw("dau_deta[0] >> hq(,-0.5,0.5)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";leading daughter #Delta#eta;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/first_dau_deta.pdf")

    t.Draw("dau_pt >> hg(,0,50)", cut + " * (partonId==21)", "", limit)
    t.Draw("dau_pt >> hq(,0,50)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";daughter p_{T} [GeV];# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/dau_pt.pdf")

    t.Draw("dau_deta >> hg(,-0.5,0.5)", cut + " * (partonId==21)", "", limit)
    t.Draw("dau_deta >> hq(,-0.5,0.5)", cut + " * (partonId!=21)", "", limit)
    hg, hq = getPlots(";daughter #Delta#eta;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/dau_deta.pdf")


    t.Draw("dau_pt >> hg(,0,50)", cut + " * (partonId==21) * (dau_charge==0)", "", limit)
    t.Draw("dau_pt >> hq(,0,50)", cut + " * (partonId!=21) * (dau_charge==0)", "", limit)
    hg, hq = getPlots(";daughter p_{T} [GeV];# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.SetLogy(True)
    c.Print(direc+"/dau_pt_neutral.pdf")
    c.SetLogy(False)

    t.Draw("dau_deta >> hg(,-0.5,0.5)", cut + " * (partonId==21) * (dau_charge==0)", "", limit)
    t.Draw("dau_deta >> hq(,-0.5,0.5)", cut + " * (partonId!=21) * (dau_charge==0)", "", limit)
    hg, hq = getPlots(";daughter #Delta#eta;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/dau_deta_neutral.pdf")

    t.Draw("dau_pt >> hg(,0,50)", cut + " * (partonId==21) * (dau_charge!=0)", "", limit)
    t.Draw("dau_pt >> hq(,0,50)", cut + " * (partonId!=21) * (dau_charge!=0)", "", limit)
    hg, hq = getPlots(";daughter p_{T} [GeV];# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.SetLogy(True)
    c.Print(direc+"/dau_pt_charged.pdf")
    c.SetLogy(False)

    t.Draw("dau_deta >> hg(,-0.5,0.5)", cut + " * (partonId==21) * (dau_charge!=0)", "", limit)
    t.Draw("dau_deta >> hq(,-0.5,0.5)", cut + " * (partonId!=21) * (dau_charge!=0)", "", limit)
    hg, hq = getPlots(";daughter #Delta#eta;# Jets")
    hq.Draw("")
    hg.Draw("same")
    c.Print(direc+"/dau_deta_charged.pdf")

    del c

if __name__ == "__main__":
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_ECalCluster5x5.root")
    plots(f.jetAnalyser, "qgPlots/ECalCluster/", cut='abs(eta) < 2.4')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_ECalCluster3x3.root")
    plots(f.jetAnalyser, "qgPlots/ECalCluster3x3/", cut='abs(eta) < 2.4')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat.root")
    plots(f.jetAnalyser, "qgPlots/Default/", cut='abs(eta) < 2.4')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_with_pileup.root")
    plots(f.jetAnalyser, "qgPlots/WPileup/", cut='abs(eta) < 2.4')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_with_pileup_ECalCluster.root")
    plots(f.jetAnalyser, "qgPlots/WPileupECalCluster/", cut='abs(eta) < 2.4')
    fcms = r.TFile("/cms/scratch/gkfthddk/CMSSW_8_0_26/src/jetIdentification/jetAnalyser/test/gkfthddk/jetall.root")
    plots(fcms.jetAnalyser.Get("jetAnalyser"), "qgPlots/CMSSW/", limit=500000, cut='abs(eta) < 2.4')
    f=r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/Delphes_CMSJet.root")
    plots(f.jetAnalyser, "qgPlots/CMSGen/", limit=500000, cut='abs(eta) < 2.4')
    f=r.TFile("Analysis_CMSGen_ECalCluster.root")
    plots(f.jetAnalyser, "qgPlots/CMSGen_ECalCluster/", limit=500000, cut='abs(eta) < 2.4')
    #
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_ECalCluster5x5.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_ECalCluster/", cut='abs(eta) < 2.4 && pt > 100')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_ECalCluster3x3.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_ECalCluster3x3/", cut='abs(eta) < 2.4 && pt > 100')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_Default/", cut='abs(eta) < 2.4 && pt > 100')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_with_pileup.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_WPileup/", cut='abs(eta) < 2.4 && pt > 100')
    f = r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/analysis_PythiaQCD_CUETP8M1_flat_with_pileup_ECalCluster.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_WPileupECalCluster/", cut='abs(eta) < 2.4 && pt > 100')
    fcms = r.TFile("/cms/scratch/gkfthddk/CMSSW_8_0_26/src/jetIdentification/jetAnalyser/test/gkfthddk/jetall.root")
    plots(fcms.jetAnalyser.Get("jetAnalyser"), "qgPlots/HighPt_CMSSW/", limit=500000, cut='abs(eta) < 2.4 && pt > 100')
    f=r.TFile("/cms/ldap_home/iawatson/scratch/jetAnalysis/Delphes_CMSJet.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_CMSGen/", limit=500000, cut='abs(eta) < 2.4 && pt > 100')
    f=r.TFile("Analysis_CMSGen_ECalCluster.root")
    plots(f.jetAnalyser, "qgPlots/HighPt_CMSGen_ECalCluster/", limit=500000, cut='abs(eta) < 2.4 && pt > 100')
