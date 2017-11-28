void merge(TString which, int num_files){
    TString fmt = TString::Format("./step3_shuffle/%s_%s.root", which.Data(), "%d");
    TString output_path = TString::Format("./step4_second_merge/%s.root", which.Data());

    TChain mychain("jetAnalyser");
    for(int i=1; i <= num_files; i++){
        TString path = TString::Format(fmt, i);
        mychain.Add(path);
    }
    mychain.Merge(output_path);
}

void macro(){

    if(gSystem->AccessPathName(output_dir)){
        gSystem->mkdir(output_dir);
    }

    merge("dijet", 20);
    merge("zjet", 20);
}
