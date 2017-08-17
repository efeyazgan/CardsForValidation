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
#process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#if not options.warnings: process.MessageLogger.cerr.threshold = 'ERROR'
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nevents)
)

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring(
*(
'/eos/cms/store/mc/RunIIWinter15wmLHE/WJetsToMuNu_13TeV_NNPDF31nlo-madgraphFxFx/LHE/MCRUN2_71_V1-v1/50000/06ADE584-D979-E711-9CDC-02163E013F55.root'
)

    ),
    inputCommands = cms.untracked.vstring('keep *', 
        'drop LHEXMLStringProduct_*_*_*'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/SMP-RunIIWinter15GS-00019-fragment.py nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('SMP-RunIIWinter15GS-00019-fragment_py_GEN.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)
process.RECOSIMoutput.outputCommands.append('keep *_generator*_*_*')

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *


process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(True),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 999.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 30.', #this is the actual merging scale
            'JetMatching:doFxFx = on',
            'JetMatching:qCutME = 10.',#this must match the ptj cut in the lhe generation step
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'TimeShower:mMaxGamma = 4.0',

#-----------------------------CP4-------------------------------------
#            'Tune:pp 14',
#            'Tune:ee 7',
#            'PDF:pSet=20',
#            'MultipartonInteractions:ecmPow=0.02012',
#            'MultipartonInteractions:bProfile=2',
#            'MultipartonInteractions:pT0Ref=1.483',
#            'MultipartonInteractions:coreRadius=0.5971',
#            'MultipartonInteractions:coreFraction=0.3053',
#            'ColourReconnection:range=5.613',
#            'SigmaTotal:zeroAXB=off', #only relevant for MB events
#            'SpaceShower:alphaSorder=2',
#            'SpaceShower:alphaSvalue=0.118',
#            'SigmaProcess:alphaSvalue=0.118',
#            'SigmaProcess:alphaSorder=2',
#            'MultipartonInteractions:alphaSvalue=0.118',
#            'MultipartonInteractions:alphaSorder=2',
#            'TimeShower:alphaSorder=2',
#            'TimeShower:alphaSvalue=0.118',
#            'SpaceShower:rapidityOrder=off',
#-------------------CP5-----------------------------------------------
        'Tune:pp 14',
        'Tune:ee 7',
        'MultipartonInteractions:ecmPow=0.03344',
        'PDF:pSet=20',
        'MultipartonInteractions:bProfile=2',
        'MultipartonInteractions:pT0Ref=1.41',
        'MultipartonInteractions:coreRadius=0.7634',
        'MultipartonInteractions:coreFraction=0.63',
        'ColourReconnection:range=5.176',
        'SigmaTotal:zeroAXB=off',
        'SpaceShower:alphaSorder=2',
        'SpaceShower:alphaSvalue=0.118',
        'SigmaProcess:alphaSvalue=0.118',
        'SigmaProcess:alphaSorder=2',
        'MultipartonInteractions:alphaSvalue=0.118',
        'MultipartonInteractions:alphaSorder=2',
        'TimeShower:alphaSorder=2',
        'TimeShower:alphaSvalue=0.118',
#--------------------------------------------------------------------
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
            'pythia8CUEP8M1Settings',
            'pythia8aMCatNLOSettings',
            'processParameters'
        )
    )
)

#process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")
#
#process.rivetAnalyzer.AnalysisNames     = cms.vstring('CMS_2016_I1479624')
#process.rivetAnalyzer.OutputFile        = options.yoda
#process.rivetAnalyzer.UseExternalWeight = True
##process.rivetAnalyzer.useLHEweights     = options.uselhewgt
##process.rivetAnalyzer.LHEweightNumber   = options.lhewgt
#process.rivetAnalyzer.LHECollection     = cms.InputTag('externalLHEProducer')
#process.rivetAnalyzer.CrossSection      = 61526.7

process.rivetAnalyzer = cms.EDAnalyzer("RivetAnalyzer",
#    AnalysisNames = cms.vstring('CMS_2016_I1434354'),
#    AnalysisNames = cms.vstring('CMS_2016_I1491950'),
     AnalysisNames = cms.vstring('CMS_2016_I1479624'),                          
    CrossSection = cms.double(20508.9),
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

# Path and EndPath definitions
process.generation_step = cms.Path(process.generator*process.rivetAnalyzer)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
#process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
#process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RECOSIMoutput_step)
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 


##############################
iFileName = "fileNameDump_cfg.py"
file = open(iFileName,'w')
file.write(str(process.dumpPython()))
file.close()
