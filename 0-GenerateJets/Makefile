ALL=DelphesPythia8 DelphesCMSFWLite

all : $(ALL)

DelphesPythia8 : DelphesPythia8.cpp
	g++ -o DelphesPythia8 DelphesPythia8.cpp -L/cms/scratch/iwatson/install/Delphes-3.4.1/ -lpythia8 -L/cms/scratch/iwatson/install/pythia8226/lib -I/cms/scratch/iwatson/install/include/Pythia8 -I/cms/scratch/iwatson/install/include `root-config --cflags --libs` -I/cms/scratch/iwatson/install/Delphes-3.4.1/ -I/cms/scratch/iwatson/install/Delphes-3.4.1/external -lEG -lDelphes

ifneq ($(CMSSW_FWLITE_INCLUDE_PATH),)
HAS_CMSSW = true
CXXFLAGS += -std=c++0x -I$(subst :, -I,$(CMSSW_FWLITE_INCLUDE_PATH))
OPT_LIBS += -L$(subst include,lib,$(subst :, -L,$(CMSSW_FWLITE_INCLUDE_PATH)))
ifneq ($(CMSSW_RELEASE_BASE),)
CXXFLAGS += -I$(CMSSW_RELEASE_BASE)/src
endif
ifneq ($(LD_LIBRARY_PATH),)
OPT_LIBS += -L$(subst include,lib,$(subst :, -L,$(LD_LIBRARY_PATH)))
endif
OPT_LIBS += -lGenVector -lFWCoreFWLite -lDataFormatsFWLite -lDataFormatsCommon -lDataFormatsPatCandidates -lDataFormatsLuminosity -lSimDataFormatsGeneratorProducts -lCommonToolsUtils -lDataFormatsCommon
endif

DelphesCMSFWLite : DelphesCMSFWLite.cpp
	g++ -o DelphesCMSFWLite DelphesCMSFWLite.cpp -L/cms/scratch/iwatson/install/Delphes-3.4.1/ -lpythia8 -L/cms/scratch/iwatson/install/pythia8226/lib -I/cms/scratch/iwatson/install/include/Pythia8 -I/cms/scratch/iwatson/install/include `root-config --cflags --libs` -I/cms/scratch/iwatson/install/Delphes-3.4.1/ -I/cms/scratch/iwatson/install/Delphes-3.4.1/external -lEG -lDelphes -lGenVector -lFWCoreFWLite -lDataFormatsFWLite -lDataFormatsCommon -lDataFormatsPatCandidates -lDataFormatsLuminosity -lSimDataFormatsGeneratorProducts -lCommonToolsUtils -lDataFormatsCommon -I$(CMSSW_RELEASE_BASE)/src -I$(subst :, -I,$(CMSSW_FWLITE_INCLUDE_PATH)) -L$(subst include,lib,$(subst :, -L,$(CMSSW_FWLITE_INCLUDE_PATH))) -L$(subst include,lib,$(subst :, -L,$(LD_LIBRARY_PATH)))

clean :
	rm -rf $(ALL)
