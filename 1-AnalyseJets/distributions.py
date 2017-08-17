import ROOT
ROOT.gStyle.SetOptStat(0)

c = ROOT.TCanvas()

fqcd = ROOT.TFile("root/PythiaQCD_CUETP8M1_flat.root")
fqcd.jetAnalyser.SetLineWidth(2)

fqcd.jetAnalyser.SetLineColor(ROOT.kBlue)
fqcd.jetAnalyser.Draw("abs(partonId) >> hP", "matched", "")
fqcd.jetAnalyser.SetLineColor(ROOT.kRed)
fqcd.jetAnalyser.Draw("flavorId >> hF", "matched", "SAME")
fqcd.jetAnalyser.SetLineColor(ROOT.kOrange)
fqcd.jetAnalyser.Draw("flavorAlgoId >> hA", "matched", "SAME")
fqcd.jetAnalyser.SetLineColor(ROOT.kMagenta)
fqcd.jetAnalyser.Draw("flavorPhysId >> hPh", "matched", "SAME")
fqcd.jetAnalyser.SetLineColor(ROOT.kGreen)
fqcd.jetAnalyser.Draw("flavorId >> hFN", "!matched", "SAME")

l = ROOT.TLegend(.5, .5, .8, .8)
l.AddEntry(ROOT.gROOT.FindObject("hP"), "PartonId")
l.AddEntry(ROOT.gROOT.FindObject("hF"), "FlavorId")
l.AddEntry(ROOT.gROOT.FindObject("hA"), "FlavorAlgoId")
l.AddEntry(ROOT.gROOT.FindObject("hPh"), "FlavorPhysId")
l.AddEntry(ROOT.gROOT.FindObject("hFN"), "Unmatched")
l.Draw()
c.Print('figures/Ids.pdf')

ptcut = 100
fqcd.jetAnalyser.SetLineColor(ROOT.kBlue)
fqcd.jetAnalyser.Draw("abs(partonId) >> hP", "matched && (pt > "+str(ptcut)+")", "")
fqcd.jetAnalyser.SetLineColor(ROOT.kRed)
fqcd.jetAnalyser.Draw("flavorId >> hF", "matched && (pt > "+str(ptcut)+")", "SAME")
fqcd.jetAnalyser.SetLineColor(ROOT.kGreen)
fqcd.jetAnalyser.Draw("flavorId >> hFN", "!matched && (pt > "+str(ptcut)+")", "SAME")

l = ROOT.TLegend(.5, .5, .8, .8)
l.AddEntry(ROOT.gROOT.FindObject("hP"), "PartonId")
l.AddEntry(ROOT.gROOT.FindObject("hF"), "FlavorId")
l.AddEntry(ROOT.gROOT.FindObject("hFN"), "Unmatched")
l.Draw()
c.Print('figures/Ids_HighPt.pdf')
