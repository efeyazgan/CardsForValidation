import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
import os
import sys


options = VarParsing.VarParsing ('standard')

options.register('nevents', 500, VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.int, "Number of events")

options.register('yoda', 'run.yoda', VarParsing.VarParsing.multiplicity.singleton,VarParsing.VarParsing.varType.string, "YODA output file")


# define the syntax for parsing
# you need to enter in the cfg file:
# search for arguments entered after cmsRun
if( hasattr(sys, "argv") ):
    # split arguments by comma - seperating different variables
    for args in sys.argv :
        arg = args.split(',')
        # split further by = to separate variable name and value
        for val in arg:
            val = val.split('=')
            # set variable var to value val (expected crab syntax: var=val)
            if(len(val)==2):
                setattr(options,val[0], val[1])

print options

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('TopMonteCarlo.Configuration.Hadronizer_pythia8_FxFx_TuneCP4_NNPDF31_cff')
#process.load('Configuration.Generator.Hadronizer_pythia8_Powheg_TuneCP4_NNPDF31_cff')
process.load('Configuration.Generator.Hadronizer_pythia8_FxFx_TuneCP5_NNPDF31_cff')
process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nevents)
)

from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet( 
#SkipEvent=cms.untracked.vstring('StdException')
)

process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
#    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/8TeV/powheg/V2/TT_hdamp_TuneT4_NNPDF31/TT_hdamp_TuneT4_NNPDF31.tgz'),
    args = cms.vstring('/afs/cern.ch/user/e/efe/workspace_afs/CMSSW_9_2_6_patch1/src/tt012j_1l_t_5f_ckm_NLO_FXFX_NNPDF31_NNLO_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(options.nevents),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/POWHEGsamePDF.py nevts:500'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

process.rivetAnalyzer = cms.EDAnalyzer("RivetAnalyzer",
#    AnalysisNames = cms.vstring('CMS_2016_I1434354'),
    AnalysisNames = cms.vstring('CMS_2016_I1491950'),
    CrossSection = cms.double(831.36),
    DoFinalize = cms.bool(True),
    GenEventInfoCollection = cms.InputTag("generator"),
    HepMCCollection = cms.InputTag("generator:unsmeared"),
#    OutputFile = cms.string('tt.yoda'),
    OutputFile = cms.string(options.yoda),
    ProduceDQMOutput = cms.bool(False),
    UseExternalWeight = cms.bool(False),
    LHECollection = cms.InputTag('externalLHEProducer'), #52X in private LHE files is source 71X is externalLHEProducer'),
    useLHEweights = cms.bool(False),
    LHEweightNumber = cms.int32(0),
    PSweightNumber = cms.int32(0)
                                        
                                       
)


# Output definition
process.LHEoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.LHEEventContent.outputCommands,
    fileName = cms.untracked.string('file:events_decayed.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN')
    )
)


process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('POWHEGsamePDF_py_GEN.root.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.generation_step = cms.Path(process.generator*process.rivetAnalyzer) 
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.endjob_step)

# customisation of the process.


# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

iFileName = "fileNameDump_cfg.py"
file = open(iFileName,'w')
file.write(str(process.dumpPython()))
file.close()

# End of customisation functions
