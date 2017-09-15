#!/usr/bin/env python

import ROOT

if False:
    f = ROOT.TFile("/home/gkfthddk/tutorials/jet1.root")
    # f = ROOT.TFile("/home/gkfthddk/tutorials/jetall.root")

    # Adjustable Settings

    #outf = ROOT.TFile("out-100_200.root", 'recreate')
    # extr = " && pt > 100 && pt < 200"

    #outf = ROOT.TFile("out-1000.root", 'recreate')
    #extr = " && pt > 1000"

    outf = ROOT.TFile("tmva_CMS.root", 'recreate')
    extr = ""
    dataname = 'CMS'
    ntrain = 20000
    ntest = 5000
else:
    ggf = ROOT.TFile("AnalyseRoot/pp_gg_cuep8m1.root")
    qqf = ROOT.TFile("AnalyseRoot/pp_qq_cuep8m1.root")
    outf = ROOT.TFile("root/pp_xx_cuep8m1.root", "recreate")
    extr = " && (order==1 || order==2) && balanced && n_dau > 1"
    dataname = "delphes"
    ntrain = 8100
    ntest = 1000

# ---- 

fac = ROOT.TMVA.Factory("TMVAClassification", outf, '!V:!Silent:Color:AnalysisType=Classification') # :Transformations=I;D;P;G;D')
dl = ROOT.TMVA.DataLoader(dataname)

dl.AddVariable("cmult", 'I')
dl.AddVariable("nmult", 'I')
# dl.AddVariable("mult", 'I')
dl.AddVariable("axis1", 'F')
dl.AddVariable("axis2", 'F')
dl.AddVariable("ptD", 'F')
dl.AddVariable("pt_dr_log", 'F')
# dl.AddVariable("eta", 'F')
# dl.AddVariable("pt", 'F')

if type(ggf.jetAnalyser) == ROOT.TDirectoryFile:
    dl.AddSignalTree(f.jetAnalyser.Get("jetAnalyser"))
    dl.AddBackgroundTree(f.jetAnalyser.Get("jetAnalyser"))
else:
    dl.AddSignalTree(ggf.Get("jetAnalyser"))
    dl.AddBackgroundTree(qqf.Get("jetAnalyser"))

idVar = 'partonId'
idVar = 'flavorId'

scut = ROOT.TCut(""+idVar+" != 0 && "+idVar+"==21 && axis2 < 1000" + extr)
bcut = ROOT.TCut(""+idVar+" != 0 && "+idVar+"!=21 && axis2 < 1000" + extr)

scut = ROOT.TCut(""+"axis2 < 1000" + extr)
bcut = ROOT.TCut(""+"axis2 < 1000" + extr)

dl.PrepareTrainingAndTestTree(scut, bcut, "nTrain_Signal={0}:nTrain_Background={0}:nTest_Signal={1}:nTest_Background={1}:SplitMode=Random:NormMode=NumEvents:!V".format(ntrain, ntest))

fac.BookMethod(dl, ROOT.TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
# fac.BookMethod(dl, ROOT.TMVA.Types.kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm")
fac.BookMethod(dl, ROOT.TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10")
# fac.BookMethod(ROOT.TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator")
fac.BookMethod(dl, ROOT.TMVA.Types.kLikelihood, "Likelihood", "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=1000")

fac.TrainAllMethods()
fac.TestAllMethods()
fac.EvaluateAllMethods()

outf.Write()
outf.Close()

ROOT.TMVA.correlations(dataname, outf.GetName())
ROOT.TMVA.variables(dataname, outf.GetName())
ROOT.TMVA.mvas(dataname, outf.GetName(), ROOT.TMVA.kMVAType)
ROOT.TMVA.mvas(dataname, outf.GetName(), ROOT.TMVA.kCompareType)
ROOT.TMVA.mvas(dataname, outf.GetName(), ROOT.TMVA.kProbaType)
ROOT.TMVA.mvas(dataname, outf.GetName(), ROOT.TMVA.kRarityType)
# ROOT.TMVA.mvaeffs(outf.GetName())
ROOT.TMVA.efficiencies(outf.GetName())
ROOT.TMVA.efficiencies(outf.GetName(), 3)

# ROOT.gROOT.ProcessLine(".L ROCCurve.C+")

outf = ROOT.TFile(outf.GetName())
mvaBDT = ROOT.vector('float')()
#mvaMLP = ROOT.vector('float')()
mvaFis = ROOT.vector('float')()
mvaT = ROOT.vector('bool')()
for ev in outf.Get(dataname+"/TrainTree"):
    mvaBDT.push_back(ev.BDT)
#    mvaMLP.push_back(ev.MLP)
    mvaFis.push_back(ev.Fisher)
    # Signal is stored as class 0
    mvaT.push_back(not ev.classID)

outt = open(outf.GetName().replace(".root", "_auc.txt"), 'w')
roc = ROOT.TMVA.ROCCurve(mvaBDT, mvaT)
auc = roc.GetROCIntegral()
outt.write("BDT AUC: "+str(auc)+'\n')

# roc = ROOT.TMVA.ROCCurve(mvaMLP, mvaT)
# auc = roc.GetROCIntegral()
# outt.write("MLP AUC: "+str(auc)+'\n')

roc = ROOT.TMVA.ROCCurve(mvaFis, mvaT)
auc = roc.GetROCIntegral()
outt.write("Fis AUC: "+str(auc)+'\n')

outt.close()
# ROOT.TMVA.TMVAGui('out.root')
