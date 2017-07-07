from subprocess import PIPE, Popen
import select
import os
import shutil


outdir = 'QCD_HT1000to2000'

mad_log = open(outdir+'_mad.log', 'w')
if os.path.exists(outdir):
    print("Cleaning up old directory")
    shutil.rmtree(outdir)

mad = Popen(["../install/MG5_aMC_v2_5_5/bin/mg5_aMC"], stdin=PIPE, stdout=PIPE)
print("Running MadGraph")
mad.stdin.write("""
import model sm-ckm_no_b_mass
define p = u c s d b u~ c~ s~ d~ b~ g
define j = u c s d b u~ c~ s~ d~ b~ g
generate p p > j j
add process p p > j j j
# add process p p > j j j j
output {0} -nojpeg
launch
done
Cards/{0}_run_card.dat
done
quit
""".format(outdir))
while True:
    nextline = mad.stdout.readline()
    if nextline == '' and mad.poll() is not None:
        break
    mad_log.write(nextline)

mad_log.close()
# Non-blocking io
# y = select.poll()
# y.register(mad.stdout, select.POLLIN)
# while True:
#     if y.poll(1): print(mad.stdout.readline().strip())
#     else: break

outfile = outdir+"/Events/run_01/unweighted_events.lhe.gz"
print("Finished generation, see log " + mad_log.name + " for more info.")
if not os.path.exists(outfile):
    print("ERROR: madgraph output not found!")
    exit(1)

os.system("gunzip "+outfile)

print("Running Delphes+Pythia8 over the Madgraph output")

cmndname = 'Cards/configLHE_'+outdir+'.cmnd'
cmnd = open(cmndname, 'w')
cmnd.write("""! 1) Settings used in the main program.

Main:numberOfEvents = 99999        ! number of events to generate
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().

Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times

! 3) Set the input LHE file

Beams:frameType = 4
Beams:LHEF = %s/Events/run_01/unweighted_events.lhe



! JetMatching:merge = on
! JetMatching:scheme = 1
! JetMatching:setMad = on
! JetMatching:qCut = 10.0
! JetMatching:coneRadius = 1.0
JetMatching:etaJetMax = 5.0
! JetMatching:nJet = 2
JetMatching:nJetMax = 3
! JetMatching:doShowerKt = 0
""" % outdir)
cmnd.close()

delphes_log = open(outdir+'_delphes.log', 'w')
delphes = Popen(["./DelphesPythia8", "./Cards/delphes_card_CMS.tcl", cmndname, "delphes_"+outdir+".root"], stdin=PIPE, stdout=PIPE)
while True:
    nextline = delphes.stdout.readline()
    if nextline == '' and delphes.poll() is not None:
        break
    delphes_log.write(nextline)

delphes_log.close()

print("Running analysis")
os.system("./analysis delphes_{0}.root analysis_{0}.root".format(outdir))
