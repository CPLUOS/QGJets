TString AttachLabel(TString input_path,
                    TString output_dir){
    // Input
    TFile* input_file = new TFile(input_path, "READ");
    TTree* input_tree = (TTree*) input_file->Get("jetAnalyser");

    TString kInputName = gSystem->BaseName(input_path);
    int input_entries = input_tree->GetEntries();

    bool kIsQQ = kInputName.Contains("qq");
    bool kIsGG = kInputName.Contains("gg");
    bool kIsZQ = kInputName.Contains("zq");

    bool kIsQuarkJets = kIsQQ or kIsZQ;
    bool kIsDijet = kIsQQ or kIsGG;

    TString criteria_name = kIsDijet ? "balanced" : "passed";
    bool criteria
    input_tree->SetBranchAddress(criteria_name, &criteria);

    // Output
    TString output_name = input_name.ReplaceAll("default", criteria_name);
    TString output_path = gSystem->ConcatFileName(output_dir, output_name);

    TFile* output_file = new TFile(output_path, "RECREATE");
    TTree* output_tree = input_tree->CloneTree(0);
    output_tree->SetDirectory(output_file);
    
    int label[2];
    if(kIsQuarkJets){
        label[0] = 1;
        label[1] = 0;
    }
    else{
        label[0] = 0;
        label[1] = 1;
    }
    
    output_tree->Branch("label", &label, "label[2]/I");
    
    for(int i=0; i < input_entries; i++){
        input_tree->GetEntry(i);
        if(not criteria) continue;

        output_tree->Fill();
    }
    
    output_file->Write();
    output_file->Close();
    
    input_file->Close();
    
    return output_path;
}



std::vector<TString> GetPaths(TString data_dir,
                              int num_files=20){
    TString fmt = TString::Format(
        "./%s/mg5_pp_%s_default_pt_50_100_%d.root",
        data_dir, "%s", "%d");

    std::vector< TString > paths;
    for(int i=1; i <= num_files; i++){
        for(auto partons : {"qq", "gg", "zq", "zg"}){
            TString qq_path = TString::Format(qq_fmt, i);
            paths.push_back(path);
        }
    }

    return paths;
}



void macro(){

    TString output_dir = "";

    if(gSystem->AccessPathName(output_dir)){
        gSystem->mkdir(output_dir);
    }

    std::vector<TString> paths = GetPaths(20);
    for(auto input_path : paths){
        AttachLabel(input_path, output_dir);
    }
}
