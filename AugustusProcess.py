#!/usr/bin/python

import tempfile
import os

# Internal dependencies
from Track import Track
import util.SubTools as subtools


class AugustusProcess(object):
    def __init__(self, inputGFF3File, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub):
        super(AugustusProcess, self).__init__()

        self.track = None

        inputGFF3File = open(inputGFF3File, 'r')
        inputFastaFile = open(inputFastaFile, 'r')

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
        chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # gff3ToGenePred processing
        subtools.gff3ToGenePred(inputGFF3File.name, genePredFile.name)

        # TODO: From there, refactor because common use with Gtf.py
        # genePredToBed processing
        subtools.genePredToBed(genePredFile.name, unsortedBedFile.name)

        # Sort processing
        subtools.sort(unsortedBedFile.name, sortedBedFile.name)

        # 2bit file creation from input fasta
        twoBitFile = subtools.faToTwoBit(inputFastaFile.name, mySpecieFolderPath)

        # Generate the twoBitInfo
        subtools.twoBitInfo(twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to generate the chromSizes
        # TODO: Check if no errors
        subtools.sortChromSizes(twoBitInfoFile.name, chromSizesFile.name)

        # bedToBigBed processing
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "augustusDbia3.bb"
        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name, chromSizesFile.name, bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackName=trackName,
            longLabel='From AugustusProcess',
            shortLabel='Augustus_dbia3',
            trackDataURL=dataURL,
            trackType='bigBed 12 +',
            visibility='dense')

        print("- %s created in %s" % (trackName, myBigBedFilePath))
