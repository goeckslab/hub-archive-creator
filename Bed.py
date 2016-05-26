#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Track import Track
from util import subtools


class Bed(object):
    def __init__(self, inputBedGeneric, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub):
        super(Bed, self).__init__()

        self.track = None

        inputBedGeneric = open(inputBedGeneric, 'r')
        self.inputBedGeneric = inputBedGeneric

        inputFastaFile = open(inputFastaFile, 'r')
        self.inputFastaFile = inputFastaFile

        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        self.chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")
        self.twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)

        self.outputFile = outputFile
        self.toolDirectory = toolDirectory
        self.extra_files_path = extra_files_path
        self.ucsc_tools_path = ucsc_tools_path
        self.trackHub = trackHub

        # Sort processing
        subtools.sort(self.inputBedGeneric.name, self.sortedBedFile.name)

        # Before the bedToBigBed processing, we need to retrieve the chrom.sizes file from the reference genome
        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        self.twoBitFile = subtools.faToTwoBit(self.inputFastaFile.name, mySpecieFolderPath)

        # Generate the chrom.sizes
        # TODO: Isolate in a function
        # We first get the twoBit Infos
        subtools.twoBitInfo(self.twoBitFile.name, self.twoBitInfoFile.name)

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        subtools.sortChromSizes(self.twoBitInfoFile.name, self.chromSizesFile.name)

        # bedToBigBed processing
        # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "bed.bb"

        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name, self.chromSizesFile.name, self.bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        # Return the BigBed track
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackName=trackName,
            longLabel='From Bed',  # TODO: Change this because it can be called by others thing that .bed => .gtf/.gff3
            shortLabel='bed file',
            trackDataURL=dataURL,
            trackType='bigBed 12',
            visibility='dense',
            thickDrawItem='on')

        print("- %s created in %s" % (trackName, myBigBedFilePath))
