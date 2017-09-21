set nb_core 0
define q = u d s
define q~ = u~ d~ s~
generate p p > l+ l- g
output MG5/pp_zg_default
launch
shower=PYTHIA8
done
./MG5/run_card_zj.dat
done
