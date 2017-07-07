all : analysis DelphesPythia8 DelphesCMSFWLite

analysis : analysis.cxx
	g++ -g -std=c++14 -o analysis analysis.cxx -L../install/Delphes-3.4.1/ -I../install/include `root-config --cflags --libs` -I../install/Delphes-3.4.1/ -I../install/Delphes-3.4.1/external -lEG -lDelphes

DelphesPythia8 : DelphesPythia8.cpp
	g++ -o DelphesPythia8 DelphesPythia8.cpp -L../install/Delphes-3.4.1/ -lpythia8 -L../install/pythia8226/lib -I../install/include/Pythia8 -I../install/include `root-config --cflags --libs` -I../install/Delphes-3.4.1/ -I../install/Delphes-3.4.1/external -lEG -lDelphes

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
	g++ -o DelphesCMSFWLite DelphesCMSFWLite.cpp -L../install/Delphes-3.4.1/ -lpythia8 -L../install/pythia8226/lib -I../install/include/Pythia8 -I../install/include `root-config --cflags --libs` -I../install/Delphes-3.4.1/ -I../install/Delphes-3.4.1/external -lEG -lDelphes -lGenVector -lFWCoreFWLite -lDataFormatsFWLite -lDataFormatsCommon -lDataFormatsPatCandidates -lDataFormatsLuminosity -lSimDataFormatsGeneratorProducts -lCommonToolsUtils -lDataFormatsCommon -I$(CMSSW_RELEASE_BASE)/src -I$(subst :, -I,$(CMSSW_FWLITE_INCLUDE_PATH)) -L$(subst include,lib,$(subst :, -L,$(CMSSW_FWLITE_INCLUDE_PATH))) -L$(subst include,lib,$(subst :, -L,$(LD_LIBRARY_PATH)))
