import os
import ROOT

def ensure(direc):
    if not os.path.exists(direc):
        os.system("mkdir -p "+direc)

ROOT.gStyle.SetOptStat(0)
ROOT.gSystem.Load("../..//install/Delphes-3.4.1/libDelphes.so")
# Delphes doesn't output the structure information to the lib for some
# reason so need to include the header for ROOT to be able to read
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')

c = ROOT.TCanvas()

def draw(fs, direc, cut, lgd, maxn=None):
    global c

    f, fpi, tcms = fs
    if maxn is None:
        maxn = f.jetAnalyser.GetEntries()
    
    n=maxn
    if fpi.jetAnalyser.GetEventList() != ROOT.MakeNullPointer():
        npi = fpi.jetAnalyser.GetEventList().GetN()
    else:
        npi = fpi.jetAnalyser.GetEntries()
    # f.jetAnalyser.Draw("nPriVtxs", str(1.0/n), "", n)
    fpi.jetAnalyser.Draw("nPriVtxs", str(1.0/npi), "")
    tcms.Draw("nPriVtxs", str(1.0/n), "SAME", n)
    lgd.Draw()
    c.Print(direc+'nPriVtx.png')

    f.jetAnalyser.Draw("partonId", str(1.0/n)+"*("+cut+")", "", n)
    fpi.jetAnalyser.Draw("partonId", str(1.0/npi)+"*("+cut+")", "SAME")
    tcms.Draw("partonId", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"partonId.png")

    f.jetAnalyser.Draw("pt", str(1.0/n)+"*("+cut+")", "", n)
    fpi.jetAnalyser.Draw("pt", str(1.0/npi)+"*("+cut+")", "SAME")
    tcms.Draw("pt", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"pt.png")

    f.jetAnalyser.Draw("eta", str(1.0/n)+"*("+cut+")", "", n)
    fpi.jetAnalyser.Draw("eta", str(1.0/npi)+"*("+cut+")", "SAME")
    tcms.Draw("eta", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"eta.png")

    f.jetAnalyser.Draw("phi", str(1.0/n)+"*("+cut+")", "", n)
    fpi.jetAnalyser.Draw("phi", str(1.0/npi)+"*("+cut+")", "SAME")
    tcms.Draw("phi", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"phi.png")

    fpi.jetAnalyser.Draw("ptD", str(1.0/npi)+"*("+cut+")", "")
    f.jetAnalyser.Draw("ptD", str(1.0/n)+"*("+cut+")", "SAME", n)
    tcms.Draw("ptD", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"ptD.png")

    fpi.jetAnalyser.Draw("pt_dr_log", str(1.0/npi)+"*("+cut+")", "")
    f.jetAnalyser.Draw("pt_dr_log", str(1.0/n)+"*("+cut+")", "SAME", n)
    tcms.Draw("pt_dr_log", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"pt_dr_log.png")


    fpi.jetAnalyser.Draw("axis1", str(1.0/npi)+"*("+cut+")", "")
    f.jetAnalyser.Draw("axis1", str(1.0/n)+"*("+cut+")", "SAME", n)
    tcms.Draw("axis1", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"axis1.png")

    fpi.jetAnalyser.Draw("axis2", str(1.0/npi)+"*("+cut+")", "")
    f.jetAnalyser.Draw("axis2", str(1.0/n)+"*("+cut+")", "SAME", n)
    tcms.Draw("axis2", str(1.0/n)+"*("+cut+")", "SAME", n)
    c.Print(direc+"axis2.png")

    tcms.Draw("nmult", str(1.0/n)+"*("+cut+")", "", n)
    f.jetAnalyser.Draw("nmult", str(1.0/n)+"*("+cut+")", "SAME", n)
    fpi.jetAnalyser.Draw("nmult", str(1.0/npi)+"*("+cut+")", "SAME")
    lgd.Draw()
    c.Print(direc+"nmult.png")

    f.jetAnalyser.Draw("cmult", str(1.0/n)+"*("+cut+")", "", n)
    fpi.jetAnalyser.Draw("cmult", str(1.0/npi)+"*("+cut+")", "SAME")
    tcms.Draw("cmult", str(1.0/n)+"*("+cut+")", "SAME", n)
    lgd.Draw()
    c.Print(direc+"cmult.png")

    # The CMS jetIdentification code rejects neutrals with pt < 1 GeV
    # for calculations, but stores them in the dau_* branches (doh!)
    tcms.Draw("dau_pt >> (,0,30)", str(1.0/n)+"*("+cut+" && ((dau_charge == 0 && dau_pt > 1)||(dau_charge != 0)))", "hist", n)
    f.jetAnalyser.Draw("dau_pt", str(1.0/n)+"*("+cut+")", "hist SAME", n)
    fpi.jetAnalyser.Draw("dau_pt", str(1.0/npi)+"*("+cut+")", "hist SAME")
    ROOT.gROOT.FindObject("c1").FindObject("").GetXaxis().SetTitle("Daughter p_{T} [GeV]")
    ROOT.gROOT.FindObject("c1").FindObject("").GetYaxis().SetTitle("Arb. Units")
    lgd.Draw()
    c.Print(direc+"dau_pt.png")

    cutplus = cut + ' && dau_charge==0 && dau_pt > 1.'
    tcms.Draw("dau_pt >> (,0,30)", str(1.0/n)+"*("+cutplus+")", "hist", n)
    f.jetAnalyser.Draw("dau_pt", str(1.0/n)+"*("+cutplus+")", "hist SAME", n)
    fpi.jetAnalyser.Draw("dau_pt", str(1.0/npi)+"*("+cutplus+")", "hist SAME")
    ROOT.gROOT.FindObject("c1").FindObject("").GetXaxis().SetTitle("Daughter p_{T} [GeV]")
    ROOT.gROOT.FindObject("c1").FindObject("").GetYaxis().SetTitle("Arb. Units")
    lgd.Draw()
    c.Print(direc+"dau_pt_neutral.png")


    cutplus = cut + ' && dau_charge==1'
    tcms.Draw("dau_pt >> (,0,30)", str(1.0/n)+"*("+cutplus+")", "hist", n)
    f.jetAnalyser.Draw("dau_pt", str(1.0/n)+"*("+cutplus+")", "hist SAME", n)
    fpi.jetAnalyser.Draw("dau_pt", str(1.0/npi)+"*("+cutplus+")", "hist SAME")
    ROOT.gROOT.FindObject("c1").FindObject("").GetXaxis().SetTitle("Daughter p_{T} [GeV]")
    ROOT.gROOT.FindObject("c1").FindObject("").GetYaxis().SetTitle("Arb. Units")
    lgd.Draw()
    c.Print(direc+"dau_pt_charged.png")

    tcms.Draw("dau_deta >> (, -.55, .55)", str(1.0/n)+"*("+cut+")", "hist", n)
    f.jetAnalyser.Draw("dau_deta", str(1.0/n)+"*("+cut+")", "hist SAME", n)
    fpi.jetAnalyser.Draw("dau_deta", str(1.0/npi)+"*("+cut+")", "hist SAME")
    ROOT.gROOT.FindObject("c1").FindObject("").GetXaxis().SetTitle("Daughter #Delta#eta")
    ROOT.gROOT.FindObject("c1").FindObject("").GetYaxis().SetTitle("Arb. Units")
    c.Print(direc+"dau_deta.png")

    f.jetAnalyser.Draw("dau_dphi >> (80, -.55, .55)", str(1.0/n)+"*("+cut+")", " hist", n)
    fpi.jetAnalyser.Draw("dau_dphi", str(1.0/npi)+"*("+cut+")", " hist SAME")
    tcms.Draw("dau_dphi", str(1.0/n)+"*("+cut+")", "hist SAME", n)
    try:
        ROOT.gROOT.FindObject("c1").FindObject("").GetXaxis().SetTitle("Daughter #Delta#phi")
        ROOT.gROOT.FindObject("c1").FindObject("").GetYaxis().SetTitle("Arb. Units")
        ROOT.gROOT.FindObject("c1").FindObject("title").DeleteText()
    except:
        pass
    lgd.Draw()
    c.Print(direc+"dau_dphi.png")


if __name__ == "__main__":
    name = 'Default'
    fpi = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat.root")

    name = 'Status20s'
    fpi = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat__Status20s.root")

    # name = 'WPileup'
    # fpi = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat_with_pileup.root")

    # name = 'ECalGang'
    # fpi = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat_ECal_Gang.root")

    # name = 'ECalClust'
    # fpi = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat_ECalCluster.root")


    # name = 'ECalClust_wPileup'
    # fpi = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat_with_pileup_ECal_Cluster.root")

    f = ROOT.TFile("root/Delphes_CMSJet.root") #  "delphes_QCD2000.root")
    fcms = ROOT.TFile("/cms/scratch/gkfthddk/CMSSW_8_0_26/src/jetIdentification/jetAnalyser/test/gkfthddk/jetall.root")

    f.jetAnalyser.SetLineColor(ROOT.kRed+2); f.jetAnalyser.SetLineWidth(2)
    fpi.jetAnalyser.SetLineColor(ROOT.kGreen+2); fpi.jetAnalyser.SetLineWidth(2)
    tcms = fcms.jetAnalyser.Get("jetAnalyser"); tcms.SetLineWidth(2)
    tcms.SetLineColor(ROOT.kBlue+2)

    lgd = ROOT.TLegend(0.6, 0.65, 0.9, 0.9); lgd.SetFillStyle(0); lgd.SetBorderSize(0)
    lgd.AddEntry(tcms, "CMSSW")
    lgd.AddEntry(f.jetAnalyser, "CMS Generator+Delphes")
    lgd.AddEntry(fpi.jetAnalyser, "Pythia+Delphes "+name)


    fs = (f, fpi, tcms)
    n = 100000

    cut = "abs(eta) < 2.4"
    direc = 'comparison/' + name + '/'
    ensure(direc)
    draw(fs, direc, cut, lgd, maxn=n)

    cut = "abs(eta) < 2.4 && (partonId == 21)"
    direc = 'comparison/' + name + '_gluon/'
    ensure(direc)
    draw(fs, direc, cut, lgd, maxn=n)

    cut = "abs(eta) < 2.4 && (partonId != 21) && (partonId != 0)"
    direc = 'comparison/' + name + '_quark/'
    ensure(direc)
    draw(fs, direc, cut, lgd, maxn=n)
