#!/bin/sh

# Run using:
# singularity exec $HOME/Images/CCMadgraph.img ./run.sh

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/code/MG5_aMC_v2_6_0/Delphes

for f in GenRoot/*pp*; do
    if [[ $f -nt root/`basename $f` ]]; then
	echo "Processing " $f
	./analysis $f root/`basename $f`
    else
	echo "Not processing" $f
    fi
done
