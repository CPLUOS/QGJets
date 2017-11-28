void merge_dijet(){
    TString fmt = "./step1_labeling/mg5_pp_%s_balanced_pt_100_500_%d.root";
    TString out_fmt = "./step2_first_merge/dijet_%d.root";

    for(int i=1; i<=20; i++){
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


void merge_z_jet(){
    TString fmt = "./step1_labeling/mg5_pp_%s_passed_pt_100_500_%d.root";
    TString out_fmt = "./step2_first_merge/z_jet_%d.root";

    for(int i=1; i<=50; i++){
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


void macro(){

    merge("dijet", 20);
    merge("zjet", 20);

}
