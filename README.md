## This contains the CMSSW cards and grid-control config cards for validating ttbar Powheg, ttbar FxFx, and wjets MLM samples. 
### Below are some instructions

kinit username@CERN.CH
cmsrel CMSSW_9_2_6_patch1

cd CMSSW_9_2_6_patch1/src

Follow the instructions in https://gitlab.cern.ch/cms-gen/Rivet/blob/master/README.md 

* In the examples here, the outputs will be written to CMSSW_9_2_6_patch1/src/batch/output : create those directories.

...Copy 16008PowhegCP5.py or 16008_Top_FxFx_CP5.py or wjets_cp5.py here. 

* Make the necessary changes in the input parameters, nevents, gridpack or lhe file location etc. 



