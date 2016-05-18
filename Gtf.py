#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Track import Track
from util.SubTools import SubTools


class Gtf(object):
    def __init__(self, inputGtfFile, inputFastaFile, extra_files_path):
        super(Gtf, self).__init__()

        self.subtools = SubTools()

        self.track = None

        self.inputGtfFile = open(inputGtfFile, 'r')
        self.inputFastaFile = open(inputFastaFile, 'r')

        self.extra_files_path = extra_files_path

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
        chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # GtfToGenePred
        self.subtools.gtfToGenePred(self.inputGtfFile.name, genePredFile.name)

        # TODO: From there, refactor because common use with AugustusProcess.py (will be renamed GFF.py)
        #  genePredToBed processing
        self.subtools.genePredToBed(genePredFile.name, unsortedBedFile.name)

        # Sort processing
        self.subtools.sort(unsortedBedFile.name, sortedBedFile.name)

        # 2bit file creation from input fasta
        twoBitFile = self.subtools.faToTwoBit(self.inputFastaFile.name, mySpecieFolderPath)

        # Generate the twoBitInfo
        self.subtools.twoBitInfo(twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to generate the chromSizes
        # TODO: Check if no errors
        self.subtools.sortChromSizes(twoBitInfoFile.name, chromSizesFile.name)

        # bedToBigBed processing
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "gtf.bb"
        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            self.subtools.bedToBigBed(sortedBedFile.name, chromSizesFile.name, bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackName=trackName,
            longLabel='From Gtf',
            shortLabel='GTF',
            trackDataURL=dataURL,
            trackType='bigBed 12 +',
            visibility='dense')

        print("- %s created in %s" % (trackName, myBigBedFilePath))
