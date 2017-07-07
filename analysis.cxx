#include "TFile.h"
#include "TTree.h"
#include "TClonesArray.h"
#include "classes/DelphesClasses.h"
#include "TMath.h"

#include <iostream>
#include <string>
#include <memory>

using std::string;

Double_t minJetPT = 20.0;
Double_t dRCut = 0.3;

Double_t DeltaPhi(Double_t phi1, Double_t phi2) {
  static const Double_t kPI = TMath::Pi();
  static const Double_t kTWOPI = 2*TMath::Pi();
  Double_t x = phi1 - phi2;
  if(TMath::IsNaN(x)){
    std::cerr << "DeltaPhi function called with NaN" << std::endl;
    return x;
  }
  while (x >= kPI) x -= kTWOPI;
  while (x < -kPI) x += kTWOPI;
  return x;
}

Double_t DeltaR(Double_t deta, Double_t dphi) {
  return TMath::Sqrt(deta*deta + dphi*dphi);
}

int main(int argc, char *argv[])
{
  if (argc != 3) {
    std::cout << "Require input and output root file" << std::endl;
    return 1;
  }

  auto in = string{argv[1]};
  auto out = string{argv[2]};

  auto inf = TFile::Open(in.c_str());
  auto intr = (TTree*) inf->Get("Delphes");
  intr->SetBranchStatus("*", true);

  // intr->SetBranchStatus("Jet", true);
  // intr->SetBranchStatus("Jet.PT", true);
  // intr->SetBranchStatus("Jet.Eta", true);
  // intr->SetBranchStatus("Jet.NNeutrals", true);
  // intr->SetBranchStatus("Jet.NCharged", true);
  // intr->SetBranchStatus("Jet.Flavor", true);
  // intr->SetBranchStatus("Jet.Constituents", true);

  // intr->SetBranchStatus("EFlowTrack", true);
  // intr->SetBranchStatus("EFlowTrack.PT", true);
  // intr->SetBranchStatus("EFlowNeutralHadron", true);
  // intr->SetBranchStatus("EFlowNeutralHadron.ET", true);
  // intr->SetBranchStatus("EFlowPhoton", true);
  // intr->SetBranchStatus("EFlowPhoton.ET", true);
  // intr->SetBranchStatus("Tower", true);
  // intr->SetBranchStatus("Tower.ET", true);
  
  TClonesArray *jets = 0;
  intr->SetBranchAddress("Jet", &jets);
  
  auto outf = TFile::Open(out.c_str(), "RECREATE");
  auto outtr = new TTree{"jetAnalyser", "jetAnalyser"};
  // Matching Jason's jetAnalyser output
#define Branch_(type, name, suffix) type name = 0; outtr->Branch(#name, &name, #name "/" #suffix);
#define BranchI(name) Branch_(Int_t, name, I)
#define BranchF(name) Branch_(Float_t, name, F)
#define BranchVF(name) std::vector<float> name; outtr->Branch(#name, "vector<float>", &name);
#define BranchVI(name) std::vector<int> name; outtr->Branch(#name, "vector<int>", &name);
  BranchI(nEvent);
  BranchF(pt);
  BranchF(eta);
  BranchF(phi);
  BranchF(pt_dr_log);
  BranchF(ptD);
  BranchF(axis1);
  BranchF(axis2);
  BranchI(nmult);
  BranchI(cmult);
  BranchI(partonId);
  BranchVF(dau_pt);
  BranchVF(dau_deta);
  BranchVF(dau_dphi);
  BranchVI(dau_charge);
  BranchI(n_dau);
  
  for (size_t iev = 0; iev < intr->GetEntries(); ++iev) {
    intr->GetEntry(iev);
    nEvent = iev;
    
    for (unsigned j = 0; j < jets->GetEntries(); ++j) {
      auto jet = (Jet*) jets->At(j);

      // some cuts, check pt
      if (jet->PT < minJetPT) continue;
      // check overlapping jets
      bool overlap = false;
      for (unsigned k = 0; k < jets->GetEntries(); ++k) {
	if (k == j) continue;
	auto otherJet = (Jet*) jets->At(k);
	float dR = DeltaR(jet->Eta - otherJet->Eta, DeltaPhi(jet->Phi, otherJet->Phi));
	if (dR < dRCut) overlap = true;
      }
      if (overlap) continue;

      pt = jet->PT;
      eta = jet->Eta;
      phi = jet->Phi;
      nmult = jet->NNeutrals;
      cmult = jet->NCharged;
      partonId = jet->Flavor;

      axis1 = 0; axis2 = 0;
      ptD = 0;
      pt_dr_log = 0;
      dau_pt.clear();
      dau_deta.clear();
      dau_dphi.clear();
      dau_charge.clear();
      n_dau = jet->Constituents.GetEntries();
      float sum_weight = 0;
      float sum_pt = 0;
      float sum_detadphi = 0;
      float sum_deta = 0, sum_deta2 = 0, ave_deta = 0, ave_deta2 = 0;
      float sum_dphi = 0, sum_dphi2 = 0, ave_dphi = 0, ave_dphi2 = 0;
      for (size_t ic = 0; ic < n_dau; ++ic) {
	auto dau = jet->Constituents.At(ic);
	// Constituents can be a tower (neutral) or a track (charged)

	float deta = 10, dphi = 10, dr = 10, dpt = 0;
	if (auto tower = dynamic_cast<Tower*>(dau)) {
	  if (tower->ET < 1.0) { // Don't accept low energy neutrals
	    continue;
	  }
	  dpt = tower->ET;
	  deta = tower->Eta - jet->Eta;
	  dphi = DeltaPhi(tower->Phi, jet->Phi);
	  dau_charge.push_back(0);
	}
	else if (auto track = dynamic_cast<Track*>(dau)) {
	  dpt = track->PT;
	  deta = track->Eta - jet->Eta;
	  dphi = DeltaPhi(track->Phi, jet->Phi);
	  dau_charge.push_back(track->Charge);
	} else {
	  std::cout << "BAD DAUGHTER! " << dau << std::endl;
	}

	float weight = dpt*dpt;
	dau_pt.push_back(dpt);
	dau_deta.push_back(deta);
	dau_dphi.push_back(dphi);
	dr = DeltaR(deta, dphi);
	pt_dr_log += std::log(dpt / dr);
	sum_weight += weight;
	sum_pt += dpt;
	sum_deta += deta*weight;
	sum_deta2 += deta*deta*weight;
	sum_dphi += dphi*weight;
	sum_dphi2 += dphi*dphi*weight;
	sum_detadphi += deta*dphi*weight;
      }

      float a = 0, b = 0, c = 0;
      if (sum_weight > 0) {
	ptD = TMath::Sqrt(sum_weight) / sum_pt;

	ave_deta = sum_deta / sum_weight;
	ave_deta2 = sum_deta2 / sum_weight;
	ave_dphi = sum_dphi / sum_weight;
	ave_dphi2 = sum_dphi2 / sum_weight;

	a = ave_deta2 - ave_deta*ave_deta;
	b = ave_dphi2 - ave_dphi*ave_dphi;
	c = -(sum_detadphi/sum_weight - ave_deta*ave_dphi);

	float delta = sqrt(fabs((a-b)*(a-b) + 4*c*c));
	axis1 = (a+b+delta > 0) ? sqrt(0.5*(a+b+delta)) : 0;
	axis2 = (a+b-delta > 0) ? sqrt(0.5*(a+b-delta)) : 0;
      }

      axis1 = -std::log(axis1);
      axis2 = -std::log(axis2);

      outtr->Fill();
    }
  }

  outtr->Write();
  outf->Close();
  
  return 0;
}
