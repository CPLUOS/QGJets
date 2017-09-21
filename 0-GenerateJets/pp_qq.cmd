set nb_core 0
define q = u d s
define q~ = u~ d~ s~
generate p p > q q~
output MG5/pp_qq_default_0
launch
shower=PYTHIA8
done
./MG5/run_card_jj.dat
done
