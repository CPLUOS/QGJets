#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TSystem.h"

#include<iostream>
using std::endl;
using std::cout;

void merge_dijet(int nfiles){
    TString fmt = "./step1_labeling/mg5_pp_%s_150_%d.root";
    TString out_fmt = "./step2_merge/dijet_%d.root";

    for(int i=1; i<=nfiles; i++){
        TChain mychain("jetAnalyser");

        TString qq_path = TString::Format(fmt, "qq", i);
        TString gg_path = TString::Format(fmt, "gg", i);
        TString out_path = TString::Format(out_fmt, i);

        mychain.Add(qq_path);
        mychain.Add(gg_path);
        mychain.Merge(out_path);

        cout << out_path << endl;
    }
}


void merge_z_jet(int nfiles){
    TString fmt = "./step1_labeling/mg5_pp_%s_150_%d.root";
    TString out_fmt = "./step2_merge/z_jet_%d.root";

    for(int i=1; i<=nfiles; i++){
        TChain mychain("jetAnalyser");

        TString qq_path = TString::Format(fmt, "zq", i);
        TString gg_path = TString::Format(fmt, "zg", i);
        TString out_path = TString::Format(out_fmt, i);

        mychain.Add(qq_path);
        mychain.Add(gg_path);
        mychain.Merge(out_path);

        cout << out_path << endl;
    }
}

void macro();
int main()
{
  macro();
}


void macro(){

  TString output_dir = "step2_merge/";
    if(gSystem->AccessPathName(output_dir)) {
        gSystem->mkdir(output_dir);
    }

    merge_dijet(1);
    merge_z_jet(1);
}
