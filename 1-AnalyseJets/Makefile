ALL=analysis

all : $(ALL)

analysis : analysis.cxx
	g++ -g -std=c++14 -o analysis analysis.cxx -L../../install/Delphes-3.4.1/ -I../../install/include `root-config --cflags --libs` -I../../install/Delphes-3.4.1/ -I../../install/Delphes-3.4.1/external -lEG -lDelphes

clean :
	rm -rf $(ALL)
