TString shuffle_tree(TString input_path, TString output_dir){
    TFile* input_file = new TFile(input_path, "READ");
    TTree* input_tree = (TTree*) input_file->Get("jetAnalyser");
    Int_t input_entries = input_tree->GetEntries();

    TString output_filename = gSystem->BaseName(input_path);
    TString output_path = gSystem->ConcatFileName(output_dir, output_filename);

    TFile* output_file = new TFile(output_path, "RECREATE");
    TTree* output_tree = input_tree->CloneTree(0);
    output_tree->SetDirectory(output_file);

    int order[input_entries];
    for(unsigned int i=0; i<input_entries; i++){
        order[i] = i;
    }

    std::random_shuffle(order, order+input_entries );

    unsigned int mycount = 0;
    for(unsigned int i=0; i<input_entries; i++){
        if(mycount % 100 == 0){
            cout << mycount << endl;
        }
        input_tree->GetEntry(order[i]);
        output_tree->Fill();
        mycount++;
    }
    output_file->Write();
    output_file->Close();

    input_file->Close();

    return output_path;
}


void shuffle_dijet(TString which, int num_files){
    TString fmt = TString::Format("./step2_first_merge/%s_%s.root", which.Data(), "%d");
    for(int i=1; i <= num_files; i++){
        TString input_path = TString::Format(fmt, i);
        cout << "In[" << i << "]: " << input_path << endl;

        TString output_path = shuffle_tree(input_path, "./step3_shuffle");
        cout << "Out[" << i << "]: " << output_path << endl << endl;
    }
}


void macro(){
    if(gSystem->AccessPathName(output_dir)){
        gSystem->mkdir(output_dir);
    }
    shuffle("dijet", 20);
    shuffle("zjet", 20);
}
