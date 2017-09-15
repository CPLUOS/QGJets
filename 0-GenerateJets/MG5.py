#!/usr/bin/env python2

cmd_ppgg_cuep8m1 = ("""
generate p p > g g
output MG5/pp_gg_cuep8m1
launch
shower=PYTHIA8
done
./MG5/run_card_dijet.dat
./MG5/pythia8_cuep8m1_card.dat
done
""", "pp_gg_cuep8m1")

cmd_ppqq_cuep8m1 = ("""
define q = u d s
define q~ = u~ d~ s~
generate p p > q q~
output MG5/pp_qq_cuep8m1
launch
shower=PYTHIA8
done
./MG5/run_card_dijet.dat
./MG5/pythia8_cuep8m1_card.dat
done
""", "pp_qq_cuep8m1")

cmd_ppzg_cuep8m1 = ("""
define q = u d s
define q~ = u~ d~ s~
generate p p > l+ l- g
output MG5/pp_zg_cuep8m1
launch
shower=PYTHIA8
done
./MG5/run_card.dat
./MG5/pythia8_cuep8m1_card.dat
done
""", "pp_zg_cuep8m1")

cmd_ppzq_cuep8m1 = ("""
define q = u d s
define q~ = u~ d~ s~
generate p p > l+ l- q
add process p p > l+ l- q~
output MG5/pp_zq_cuep8m1
launch
shower=PYTHIA8
done
./MG5/run_card.dat
./MG5/pythia8_cuep8m1_card.dat
done
""", "pp_zq_cuep8m1")

cmd, name = cmd_ppgg_cuep8m1[0], cmd_ppgg_cuep8m1[1]
cmd, name = cmd_ppqq_cuep8m1[0], cmd_ppqq_cuep8m1[1]
cmd, name = cmd_ppzq_cuep8m1[0], cmd_ppzq_cuep8m1[1]
cmd, name = cmd_ppzg_cuep8m1[0], cmd_ppzg_cuep8m1[1]
