#include "TFile.h"
#include "TTree.h"
#include "TClonesArray.h"
#include "classes/DelphesClasses.h"
#include "TMath.h"

#include <iostream>
#include <string>
#include <memory>
#include <vector>

using std::string;

Double_t minJetPT = 20.0;
Double_t maxJetEta = 2.4;
Double_t dRCut = 0.3;
bool doHadMerge = false;
bool doEcalCl = false;

bool debug=false;

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

struct cluster {
  double pt;
  double eta;
  double phi;

  int ishadronic;
};

void fillDaughters(Jet *jet, float &leading_dau_pt, float& leading_dau_eta,
		   std::vector<float> &dau_pt, std::vector<float> &dau_deta, std::vector<float> &dau_dphi,
		   std::vector<int> &dau_charge, std::vector<int> &dau_ishadronic, int& nmult, int& cmult);
void fillDaughters_HADMERGE(Jet *jet, float &leading_dau_pt, float& leading_dau_eta,
			    std::vector<float> &dau_pt, std::vector<float> &dau_deta, std::vector<float> &dau_dphi,
			    std::vector<int> &dau_charge, std::vector<int> &dau_ishadronic, int& nmult);
void fillDaughter_EcalCluster(Jet *jet, float &leading_dau_pt, float& leading_dau_eta,
			      std::vector<float> &dau_pt, std::vector<float> &dau_deta, std::vector<float> &dau_dphi,
			      std::vector<int> &dau_charge, std::vector<int> &dau_ishadronic,
			      int& nmult, int& cmult, std::vector<float> &test);

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

  if (doEcalCl)
    std::cout << "ECAL Clustering" << std::endl;
  if (doHadMerge)
    std::cout << "E/H Mergeing" << std::endl;
  
  TClonesArray *jets = 0;
  intr->SetBranchAddress("Jet", &jets);
  TClonesArray *particles = 0;
  intr->SetBranchAddress("Particle", &particles);

  TClonesArray *vertices = 0;
  intr->SetBranchAddress("Vertex", &vertices);
  
  auto outf = TFile::Open(out.c_str(), "RECREATE");
  auto outtr = new TTree{"jetAnalyser", "jetAnalyser"};
  // Matching Jason's jetAnalyser output
#define Branch_(type, name, suffix) type name = 0; outtr->Branch(#name, &name, #name "/" #suffix);
#define BranchI(name) Branch_(Int_t, name, I)
#define BranchF(name) Branch_(Float_t, name, F)
#define BranchO(name) Branch_(Bool_t, name, O)
#define BranchVF(name) std::vector<float> name; outtr->Branch(#name, "vector<float>", &name);
#define BranchVI(name) std::vector<int> name; outtr->Branch(#name, "vector<int>", &name);
  BranchI(nEvent);
  BranchI(nJets);
  BranchI(nGoodJets);
  BranchI(nPriVtxs);
  BranchF(pt);
  BranchF(eta);
  BranchF(phi);
  BranchF(pt_dr_log);
  BranchF(ptD);
  BranchF(axis1);
  BranchF(axis2);
  BranchF(leading_dau_pt);
  BranchF(leading_dau_eta);
  BranchI(nmult);
  BranchI(cmult);
  BranchI(partonId);
  BranchI(flavorId);

  BranchI(flavorAlgoId);
  BranchI(flavorPhysId);

  BranchVF(dau_pt);
  BranchVF(dau_deta);
  BranchVF(dau_dphi);
  BranchVF(test);
  BranchVI(dau_charge);
  BranchVI(dau_ishadronic);
  BranchI(n_dau);
  BranchO(matched);

  bool firstTime = true, badHardGenSeen = false;
  for (size_t iev = 0; iev < intr->GetEntries(); ++iev) {
    intr->GetEntry(iev);
    nEvent = iev;
    nJets = jets->GetEntries();
    if (vertices)
      nPriVtxs = vertices->GetEntries();
    else // no pileup mode
      nPriVtxs = 1;

    nGoodJets = 0;
    for (unsigned k = 0; k < jets->GetEntries(); ++k) {
      auto j = (const Jet *) jets->At(k);
      if (j->PT < minJetPT)
	continue;
      if (fabs(j->Eta) > maxJetEta)
	continue;
      
      nGoodJets++;
    }
    
    // match to hard process in pythia
    std::vector<const GenParticle*> hardGen;
    for (unsigned k = 0; k < particles->GetEntries(); ++k) {
      auto p = (const GenParticle *) particles->At(k);
      if (p->Status != 23) continue; // Status 23 is hard process parton in Pythia8
      if (abs(p->PID) > 5 && p->PID != 21) continue; // consider quarks and gluons only
      hardGen.push_back(p);
      if (firstTime) {
	std::cout << "WARNING: ASSUMING PYTHIA8 HARDQCD GENERATION, ONLY 2 HARD PARTONS CONSIDERED" << std::endl;
	firstTime = false;
      }
      if (hardGen.size() == 2) break;
    }
    if (!badHardGenSeen && (hardGen.size() != 2)) {
      std::cout << "hardGen " << hardGen.size() << std::endl;
      badHardGenSeen = true;
    }
    
    for (unsigned j = 0; j < jets->GetEntries(); ++j) {
      auto jet = (Jet*) jets->At(j);

      // some cuts, check pt
      if (jet->PT < minJetPT) continue;
      if (fabs(jet->Eta) > maxJetEta) continue;

      // match to hard process in pythia
      matched = false;
      const GenParticle *match = 0;
      float dRMin = 10.;
      for (auto& p : hardGen) {
      	float dR = DeltaR(jet->Eta - p->Eta, DeltaPhi(jet->Phi, p->Phi));
      	if (dR < dRMin && dR < dRCut) {
      	  matched = true;
      	  match = p;
      	}
      }
      // if (!matched) continue;
      
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
      if (match)
	partonId = match->PID;
      else
	partonId = 0;
      flavorId = jet->Flavor;
      flavorAlgoId = jet->FlavorAlgo;
      flavorPhysId = jet->FlavorPhys;

      axis1 = 0; axis2 = 0;
      ptD = 0;
      pt_dr_log = 0;
      dau_pt.clear();
      dau_deta.clear();
      dau_dphi.clear();
      dau_charge.clear();
      dau_ishadronic.clear();
      test.clear();

      if (doEcalCl)
	fillDaughter_EcalCluster(jet, leading_dau_pt, leading_dau_eta, dau_pt, dau_deta, dau_dphi, dau_charge, dau_ishadronic, nmult, cmult, test);
      else if (doHadMerge)
	fillDaughters_HADMERGE(jet, leading_dau_pt, leading_dau_eta, dau_pt, dau_deta, dau_dphi, dau_charge, dau_ishadronic, nmult);
      else
	fillDaughters(jet, leading_dau_pt, leading_dau_eta, dau_pt, dau_deta, dau_dphi, dau_charge, dau_ishadronic, nmult, cmult);
      
      float sum_weight = 0;
      float sum_pt = 0;
      float sum_detadphi = 0;
      float sum_deta = 0, sum_deta2 = 0, ave_deta = 0, ave_deta2 = 0;
      float sum_dphi = 0, sum_dphi2 = 0, ave_dphi = 0, ave_dphi2 = 0;
      for (size_t ic = 0; ic < dau_pt.size(); ++ic) {
	double dpt = dau_pt[ic];
	double deta = dau_deta[ic];
	double dphi = dau_dphi[ic];
	double weight = dpt*dpt;	
 	double dr = DeltaR(deta, dphi);
	
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

      n_dau = dau_pt.size();

      outtr->Fill();
    }
  }

  outtr->Write();
  outf->Close();
  
  return 0;
}

void fillDaughter_EcalCluster(Jet *jet, float& leading_dau_pt, float& leading_dau_eta,
			      std::vector<float> &dau_pt, std::vector<float> &dau_deta, std::vector<float> &dau_dphi,
			      std::vector<int> &dau_charge, std::vector<int> &dau_ishadronic,
			      int& nmult, int& cmult, std::vector<float> &test)
{
  nmult = 0; cmult = 0;
  size_t n_dau = jet->Constituents.GetEntries();
  // Find ECal clusters
  std::vector<int> ecalDau;
  std::vector<int> hcalDau;

  leading_dau_pt = leading_dau_eta = 0;
  
  for (size_t ic = 0; ic < n_dau; ++ic) {
    double dpt, deta, dphi;
    auto dau = jet->Constituents.At(ic);
    // Constituents can be a tower (neutral) or a track (charged)
    auto tower = dynamic_cast<Tower*>(dau);
    if (!tower) {
      auto track = dynamic_cast<Track*>(dau);
      if (!track) {
	std::cout << "ERROR: Daughter not tower or track" << std::endl;
	exit(2);
      }

      // veto tracks from pileup, based on z-spread (see pileup card for Z0 spread)
      // if (fabs(track->Z) > 1.5*0.25) {
      // 	continue;
      // }
      test.push_back(track->Z);
      
      cmult++;
      dau_pt.push_back(track->PT);
      dau_deta.push_back(track->Eta - jet->Eta);
      dau_dphi.push_back(DeltaPhi(track->Phi, jet->Phi));
      dau_charge.push_back(track->Charge);
      dau_ishadronic.push_back(0);

      if (track->PT > leading_dau_pt) {
	leading_dau_pt = track->PT;
	leading_dau_eta = track->Eta - jet->Eta;
      }
      
      continue;
    }
    if (tower->ET < 1.0) { // Don't accept low energy neutrals
      continue;
    }
    
    if ((tower->Ehad != 0.0) && (tower->Eem != 0.0))
      std::cout << "ERROR: Tower with Had " << tower->Ehad << " and EM " << tower->Eem << " energy" << std::endl;

    if (tower->Ehad == 0.0) {
      ecalDau.push_back(ic);
    } else {
      hcalDau.push_back(ic);
    }
  }

  // sort by pt of the cell
  std::sort(ecalDau.begin(), ecalDau.end(),
	    [&jet](int a, int b){ return ((Tower*) jet->Constituents.At(a))->ET > ((Tower*) jet->Constituents.At(b))->ET; });

  double tot = 0;
  for (auto ic : ecalDau) {
    auto tower = ((Tower*) jet->Constituents.At(ic));
    if (debug) std::cout << tower->ET << " " << tower->Eta << " " << tower->Phi <<std::endl;
    tot += tower->ET;
  }
  if (debug) std::cout << tot << std::endl;

  std::vector<cluster> ecalClusters;

  // go through ecal daughters and build ecalClusters
  while (!ecalDau.empty()) {
    auto clst = (Tower*) jet->Constituents.At(ecalDau[0]);
    std::vector<int> iCl;

    // in reverse so we can easily erase later
    for (int i = ecalDau.size()-1; i > 0; --i) {
      auto cell = (Tower*) jet->Constituents.At(ecalDau[i]);
      // test within a 3x3 cell, 1 cell = 0.0174 based on CMS data card
      if ((fabs(cell->Eta - clst->Eta) < 2.5*0.0174) &&
	  (DeltaPhi(cell->Phi, clst->Phi) < 2.5*0.0174))
	iCl.push_back(i);
    }
    auto next = cluster{clst->ET, clst->Eta, clst->Phi, 0};
    for (auto i : iCl)
      next.pt += ((Tower*) jet->Constituents.At(ecalDau[i]))->ET;

    for (auto i : iCl) 
      ecalDau.erase(ecalDau.begin()+i);
    ecalDau.erase(ecalDau.begin()+0);

    ecalClusters.push_back(next);
  }


  tot = 0;
  if (debug) std::cout << std::endl << std::endl;
  for (auto cl : ecalClusters) {
    if (debug) std::cout << cl.pt << " " << cl.eta << " " << cl.phi << std::endl;
    tot += cl.pt;
  }
  if (debug) std::cout << tot << std::endl;
  if (debug) std::cout << std::endl;
  if (debug) std::cout << std::endl;
  

  std::vector<cluster> hcalClusters;
  tot = 0;
  for (auto ic : hcalDau) {
    auto tower = ((Tower*) jet->Constituents.At(ic));
    if (debug) std::cout << tower->ET << " " << tower->Eta << " " << tower->Phi <<std::endl;
    tot += tower->ET;
    hcalClusters.push_back(cluster{tower->ET, tower->Eta, tower->Phi, 1});
  }
  if (debug) std::cout << tot << std::endl;

  // // merging step
  std::vector<cluster> mergeClusters;
  for (auto ecl : ecalClusters) {
    bool foundh = false;
    for (size_t ih = 0; ih < hcalClusters.size(); ++ih) {
      if ((fabs(ecl.eta - hcalClusters[ih].eta) < 2.5*0.0174) &&
  	  DeltaPhi(ecl.phi, hcalClusters[ih].phi) < 2.5*0.0174) {
  	// ecal should be better resolved in position
  	mergeClusters.push_back(cluster{ecl.pt+hcalClusters[ih].pt, ecl.eta, ecl.phi, 1});
  	foundh = true;
  	hcalClusters.erase(hcalClusters.begin()+ih);
  	break;
      }
    }
    if (!foundh)
      mergeClusters.push_back(ecl);
  }

  // for (auto ecl : ecalClusters)
  //   mergeClusters.push_back(ecl);
  
  for (auto hcl : hcalClusters)
    mergeClusters.push_back(hcl);


  if (debug) std::cout << std::endl;
  if (debug) std::cout << std::endl;
  tot = 0;
  nmult = mergeClusters.size();
  for (auto m : mergeClusters) {
    if (debug) std::cout << m.pt << " " << m.eta << " " << m.phi <<std::endl;
    tot += m.pt;

    dau_pt.push_back(m.pt);
    dau_deta.push_back(m.eta - jet->Eta);
    dau_dphi.push_back(DeltaPhi(m.phi, jet->Phi));

    dau_ishadronic.push_back(m.ishadronic);
    dau_charge.push_back(0);

    if (m.pt > leading_dau_pt) {
      leading_dau_pt = m.pt;
      leading_dau_eta = m.eta - jet->Eta;
    }
  }
  if (debug) std::cout << tot << std::endl;

  if (debug) exit(1);
}

void fillDaughters_HADMERGE(Jet *jet, float& leading_dau_pt, float& leading_dau_eta,
			    std::vector<float> &dau_pt, std::vector<float> &dau_deta, std::vector<float> &dau_dphi,
			    std::vector<int> &dau_charge, std::vector<int> &dau_ishadronic, int& nmult)
{
  leading_dau_pt = leading_dau_eta = 0.0;
  nmult = 0;
  size_t n_dau = jet->Constituents.GetEntries();
  // fill hadronic first
  int nhad = 0;
  
  for (size_t ic = 0; ic < n_dau; ++ic) {
    double dpt, deta, dphi;
    auto dau = jet->Constituents.At(ic);
    // Constituents can be a tower (neutral) or a track (charged)
    auto tower = dynamic_cast<Tower*>(dau);
    if (!tower) continue;
    if (tower->ET < 1.0) { // Don't accept low energy neutrals
      continue;
    }

    if ((tower->Ehad != 0.0) && (tower->Eem != 0.0))
      std::cout << "ERROR: Tower with Had " << tower->Ehad << " and EM " << tower->Eem << " energy" << std::endl;

    if (tower->Ehad == 0.0) {
      continue;
    }
    dpt = tower->ET;
    deta = tower->Eta - jet->Eta;
    dphi = DeltaPhi(tower->Phi, jet->Phi);
    dau_charge.push_back(0);
    dau_ishadronic.push_back(1);
    dau_pt.push_back(dpt);
    dau_deta.push_back(deta);
    dau_dphi.push_back(dphi);
    nhad++;
    nmult++;
    if (dpt > leading_dau_pt) {
      leading_dau_pt = dpt;
      leading_dau_eta = deta;
    }
  }

  // then fill emag+track
  for (size_t ic = 0; ic < n_dau; ++ic) {
    auto dau = jet->Constituents.At(ic);

    double dpt, deta, dphi, dr;
    // Constituents can be a tower (neutral) or a track (charged)
    if (auto track = dynamic_cast<Track*>(dau)) {
      dpt = track->PT;
      deta = track->Eta - jet->Eta;
      dphi = DeltaPhi(track->Phi, jet->Phi);
      dau_charge.push_back(track->Charge);
      dau_ishadronic.push_back(0);
      dau_pt.push_back(dpt);
      dau_deta.push_back(deta);
      dau_dphi.push_back(dphi);
      if (dpt > leading_dau_pt) {
	leading_dau_pt = dpt;
	leading_dau_eta = deta;
      }
    } else if (auto tower = dynamic_cast<Tower*>(dau)) {
      if (tower->ET < 1.0) { // Don't accept low energy neutrals
	continue;
      }
      if (tower->Eem == 0.0) {
	continue;
      }

      dpt = tower->ET;
      deta = tower->Eta - jet->Eta;
      dphi = DeltaPhi(tower->Phi, jet->Phi);
	  
      bool found = false;
      for (size_t ih; ih < nhad; ++ih) {
	if ((fabs(dau_deta[ih]) < 1.653) && (fabs(deta - dau_deta[ih]) < 0.08) && (DeltaPhi(dphi, dau_dphi[ih]) < 0.08)) {
	  found = true;
	} else if ((fabs(dau_deta[ih]) < 4.35) && (fabs(deta - dau_deta[ih]) < 0.16) && (DeltaPhi(dphi, dau_dphi[ih]) < 0.16)) {
	  found = true;
	}

	// if the emag tower within the bounds, add the energy to the hadr. tower
	if (found) {
	  dau_pt[ih] += dpt;
	  if (dau_pt[ih] > leading_dau_pt) {
	    leading_dau_pt = dau_pt[ih];
	    leading_dau_eta = dau_deta[ih];
	  }
	  break;
	}
      }

      if (!found) {
	nmult++;
	dau_charge.push_back(0);
	dau_ishadronic.push_back(1);
	dau_pt.push_back(dpt);
	dau_deta.push_back(deta);
	dau_dphi.push_back(dphi);
	if (dpt > leading_dau_pt) {
	  leading_dau_pt = dpt;
	  leading_dau_eta = deta;
	}
      }
    } else {
      std::cout << "BAD DAUGHTER! " << dau << std::endl;
    }
  } 
}

void fillDaughters(Jet *jet, float& leading_dau_pt, float& leading_dau_eta,
		   std::vector<float> &dau_pt, std::vector<float> &dau_deta, std::vector<float> &dau_dphi,
		   std::vector<int> &dau_charge, std::vector<int> &dau_ishadronic, int& nmult, int& cmult)
{
  size_t n_dau = jet->Constituents.GetEntries();
  double dpt = 0, deta = 0, dphi = 0;
  nmult = cmult = 0;
  leading_dau_eta = leading_dau_pt = 0;
  for (size_t ic = 0; ic < n_dau; ++ic) {
    auto dau = jet->Constituents.At(ic);
    // Constituents can be a tower (neutral) or a track (charged)

    float deta = 10, dphi = 10, dr = 10, dpt = 0;
    if (auto tower = dynamic_cast<Tower*>(dau)) {
      // if (tower->ET < 1.0) { // Don't accept low energy neutrals
      // 	continue;
      // }
      dpt = tower->ET;
      deta = tower->Eta - jet->Eta;
      dphi = DeltaPhi(tower->Phi, jet->Phi);
      dau_charge.push_back(0); nmult++;
      if (tower->Eem == 0.0)
	dau_ishadronic.push_back(1);
      else if (tower->Ehad == 0.0)
	dau_ishadronic.push_back(0);
      else
	std::cout << "ERROR: Tower with Had " << tower->Ehad << " and EM " << tower->Eem << " energy" << std::endl;
    } else if (auto track = dynamic_cast<Track*>(dau)) {
      dpt = track->PT;
      deta = track->Eta - jet->Eta;
      dphi = DeltaPhi(track->Phi, jet->Phi);
      dau_charge.push_back(track->Charge); cmult++;
      dau_ishadronic.push_back(0);
    } else {
      std::cout << "BAD DAUGHTER! " << dau << std::endl;
    }
    dau_pt.push_back(dpt);
    dau_deta.push_back(deta);
    dau_dphi.push_back(dphi);
    if (dpt > leading_dau_pt) {
      leading_dau_pt = dpt;
      leading_dau_eta = deta;
    }
  }
}
