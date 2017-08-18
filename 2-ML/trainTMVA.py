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
else:
    f = ROOT.TFile("AnalyseRoot/PythiaQCD_CUETP8M1_flat.root")
    outf = ROOT.TFile("root/TMVA_PythiaQCD_CUETP8M1_flat.root", 'recreate')
    extr = ' && pt > 100'
    dataname = 'delphes'

# ntrain = 100000
# ntest = 30000

#ntrain = 100000
#ntest = 20000

ntrain = 50000
ntest = 10000

# ---- 

fac = ROOT.TMVA.Factory("TMVAClassification", outf, '!V:!Silent:Color:AnalysisType=Classification') # :Transformations=I;D;P;G;D')
# dl = ROOT.TMVA.DataLoader(dataname)

# In newer root versions, you need to use the DataLoader Class here

fac.AddVariable("cmult", 'I')
fac.AddVariable("nmult", 'I')
# fac.AddVariable("mult", 'I')

fac.AddVariable("axis1", 'F')
fac.AddVariable("axis2", 'F')
fac.AddVariable("ptD", 'F')
fac.AddVariable("pt_dr_log", 'F')

# dl.AddVariable("eta", 'F')
# dl.AddVariable("pt", 'F')

if type(f.jetAnalyser) == ROOT.TDirectoryFile:
    fac.AddSignalTree(f.jetAnalyser.Get("jetAnalyser"))
    fac.AddBackgroundTree(f.jetAnalyser.Get("jetAnalyser"))
else:
    fac.AddSignalTree(f.Get("jetAnalyser"))
    fac.AddBackgroundTree(f.Get("jetAnalyser"))

idVar = 'partonId'
idVar = 'flavorId'
    
scut = ROOT.TCut(""+idVar+" != 0 && "+idVar+"==21 && axis2 < 1000" + extr)
bcut = ROOT.TCut(""+idVar+" != 0 && "+idVar+"!=21 && axis2 < 1000" + extr)

fac.PrepareTrainingAndTestTree(scut, bcut, "nTrain_Signal={0}:nTrain_Background={0}:nTest_Signal={1}:nTest_Background={1}:SplitMode=Random:NormMode=NumEvents:!V".format(ntrain, ntest))

fac.BookMethod(ROOT.TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")
# fac.BookMethod(dl, ROOT.TMVA.Types.kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm")
fac.BookMethod(ROOT.TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:VarTransform=None:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10")
# fac.BookMethod(ROOT.TMVA.Types.kMLP, "MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+5:TestRate=5:!UseRegulator")
fac.BookMethod(ROOT.TMVA.Types.kLikelihood, "Likelihood", "H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=1000")

fac.TrainAllMethods()
fac.TestAllMethods()
fac.EvaluateAllMethods()

outf.Write()
outf.Close()

ROOT.TMVA.correlations(outf.GetName())
ROOT.TMVA.variables(outf.GetName())
ROOT.TMVA.mvas(outf.GetName(), ROOT.TMVA.kMVAType)
ROOT.TMVA.mvas(outf.GetName(), ROOT.TMVA.kCompareType)
ROOT.TMVA.mvas(outf.GetName(), ROOT.TMVA.kProbaType)
ROOT.TMVA.mvas(outf.GetName(), ROOT.TMVA.kRarityType)
# ROOT.TMVA.mvaeffs(outf.GetName())
ROOT.TMVA.efficiencies(outf.GetName())
ROOT.TMVA.efficiencies(outf.GetName(), 3)

ROOT.gROOT.ProcessLine(".L ROCCurve.C+")

outf = ROOT.TFile(outf.GetName())
mvaBDT = ROOT.vector('float')()
#mvaMLP = ROOT.vector('float')()
mvaFis = ROOT.vector('float')()
mvaT = ROOT.vector('bool')()
for ev in outf.TrainTree:
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
