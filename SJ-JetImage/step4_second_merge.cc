#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TSystem.h"

#include<iostream>
using std::endl;
using std::cout;

void merge(TString which, int num_files){
  TString output_dir("step4_merge/");
    if(gSystem->AccessPathName(output_dir)) {
        gSystem->mkdir(output_dir);
    }

    TString fmt = TString::Format("./step3_shuffle/%s_%s.root", which.Data(), "%d");
    TString output_path = TString::Format("./step4_merge/%s.root", which.Data());

    TChain mychain("jetAnalyser");
    for(int i=1; i <= num_files; i++){
        TString path = TString::Format(fmt, i);
        mychain.Add(path);
    }
    mychain.Merge(output_path);
}

void macro();
int main()
{
  macro();
}


void macro(){
    merge("dijet", 1);
    merge("z_jet", 1);
}
