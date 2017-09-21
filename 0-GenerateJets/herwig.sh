#!/bin/bash

LC_ALL=C

NAME=pp_qq

singularity run $HOME/Images/Herwig.img read $NAME.in
singularity run $HOME/Images/Herwig.img run -N 10000 $NAME.run
singularity exec $HOME/Images/CCMadgraph.img /code/MG5_aMC_v2_6_0/Delphes/DelphesHepMC Cards/delphes_card_CMS.tcl root/Herwig_$NAME.root $NAME.hepmc
rm -rf Herwig-scratch $NAME-EvtGen.log $NAME.hepmc $NAME.log $NAME.out $NAME.tex $NAME.run
