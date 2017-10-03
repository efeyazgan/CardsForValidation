## This contains the CMSSW cards and grid-control config cards for validating ttbar Powheg, ttbar FxFx, and wjets MLM samples. 
### Below are some instructions

kinit username@CERN.CH

cmsrel CMSSW_9_2_6_patch1

cd CMSSW_9_2_6_patch1/src

* Follow the instructions in https://gitlab.cern.ch/cms-gen/Rivet/blob/master/README.md 
  * ignoring the CMSSW version
  * And you may need to use git clone https://gitlab.cern.ch/cms-gen/Rivet.git 
* In the examples here, the outputs will be written to CMSSW_9_2_6_patch1/src/batch/output : create those directories.
* Copy 16008PowhegCP5.py or 16008_Top_FxFx_CP5.py or wjets_cp5.py here. 
* Make the necessary changes in the input parameters, nevents, gridpack or lhe file location etc. Gridpacks for the examples above can be accessed from /afs/cern.ch/user/e/efe/workspace_afs/public/gridpacks (Note that for FxFx there are two gridpacks, one of top and one for antitop, so, two separate submissions should be done but at the end yoda files should be just merged). 

cd GeneratorInterface/RivetInterface/data

ln -s /afs/cern.ch/user/e/efe/workspace_afs/CMSSW_9_2_6_patch1/src/Rivet/TOP/data/*.yoda .

ln -s /afs/cern.ch/user/e/efe/workspace_afs/CMSSW_9_2_6_patch1/src/Rivet/SMP/data/*.yoda .



If you want to use grid-control do:

svn co https://ekptrac.physik.uni-karlsruhe.de/svn/grid-control/tags/stable/grid-control

cd grid-control

./go.py Production_TT_Powheg_13TeV_CP5.conf -Gc

- this command is used both to submit jobs and also to check the status of the jobs.

For killing jobs: ./go.py Production_TT_Powheg_13TeV_CP5.conf -d all 

Once jobs are done:

source Rivet/rivetSetup.sh

cd batch/output

yodamerge -o merged.yoda outputfolder/*.yoda

rivet-mkhtml merged.yoda (merged2.yoda ets if you have multiple files)




