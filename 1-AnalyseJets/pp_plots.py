#!/usr/bin/env python2

import ROOT as r

r.gStyle.SetOptStat(0)

fqq = r.TFile("root/pp_qq_cuep8m1.root")
fgg = r.TFile("root/pp_gg_cuep8m1.root")

fzq = r.TFile("root/pp_zq_cuep8m1.root")
fzg = r.TFile("root/pp_zg_cuep8m1.root")

fqq.jetAnalyser.SetLineColor(r.kBlue+2)
fgg.jetAnalyser.SetLineColor(r.kRed+2)
fzq.jetAnalyser.SetLineColor(r.kGreen+2)
fzg.jetAnalyser.SetLineColor(r.kMagenta+2)

all = [fqq, fgg, fzg, fzq]
names = {fqq : "QQ", fgg : "GG", fzq : "ZQ", fzg : "ZG"}
isZ = lambda f: f == fzq or f == fzg

def plotAll(var, cut="", name=None, withZ=True, onlyZ=False, binning=None):
    global all, c
    opt = "hist"
    leg = r.TLegend(.7, .7, .95, .95)
    for f in all:
        if not withZ and isZ(f): continue
        if onlyZ and not isZ(f): continue
        nEntries = f.jetAnalyser.Draw(var + ((">>"+binning) if binning is not None else ""), cut, opt)
        opt += " same"
        leg.AddEntry(f.jetAnalyser, names[f] + " (" + str(nEntries) + ")")
        binning = None
    leg.Draw()
    c.Update()
    if name is not None:
        c.Print(name)

c = r.TCanvas()

plotAll("nJets", "order==1", "plots/nJets.pdf")

plotAll("pt", "order==1", "plots/pt_1.pdf")

plotAll("pt", "order==2", "plots/pt_2.pdf")

plotAll("pt", "order==3", "plots/pt_3.pdf")

plotAll("ptD", "order <= 2", "plots/ptD.pdf", withZ=False)

plotAll("ptD", "", "plots/ptD_ALL.pdf", withZ=False)

plotAll("pt_dr_log", "order <= 2", "plots/pt_dr_log.pdf", withZ=False)

plotAll("axis1", "order <= 2", "plots/axis1.pdf", withZ=False)
plotAll("axis2", "order <= 2", "plots/axis2.pdf", withZ=False)

plotAll("axis2", "order <= 1", "plots/axis2_zj.pdf", onlyZ=True)

plotAll("n_dau", "order <= 2", "plots/n_dau.pdf", withZ=False)
plotAll("n_dau", "order <= 1", "plots/n_dau_zj.pdf", onlyZ=True)

plotAll("n_dau", "order <= 1 && axis2 < 0.05", "plots/n_dau_zj_lowaxis2.pdf", onlyZ=True)
plotAll("nmult", "order <= 1 && axis2 < 0.05", "plots/dau_charge_zj_lowaxis2.pdf", onlyZ=True)
plotAll("dau_pt", "order <= 1 && axis2 < 0.05", "plots/dau_pt_zj_lowaxis2.pdf", onlyZ=True)
plotAll("dau_pt", "order <= 1", "plots/dau_pt_zj.pdf", onlyZ=True)

plotAll("lepton_overlap", "order <= 1", "plots/lepton_overlap_zj.pdf", onlyZ=True)

plotAll("pass_Zjets", "order <= 1", onlyZ=True)
plotAll("axis2", "pass_Zjets && order <= 1", "plots/axis2_zj_pass.pdf", onlyZ=True)
plotAll("ptD", "pass_Zjets && order <= 1", "plots/ptD_zj_pass.pdf", onlyZ=True)
plotAll("cmult+nmult", "pass_Zjets && order <= 1", "plots/mult_zj_pass.pdf", onlyZ=True, binning="(41,-0.5,40.5)")

plotAll("ptD", "balanced", "plots/ptD.pdf", withZ=False)
plotAll("ptD", "pass_Zjets", "plots/ptD_passZ.pdf", onlyZ=True)
