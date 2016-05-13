#!/usr/bin/python

import os
import subprocess
import tempfile

# Internal dependencies
from Track import Track
from util.SubTools import SubTools

class Bed(object):
    def __init__(self, inputBedGeneric, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub):
        super(Bed, self).__init__()

        self.subtools = SubTools()

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
        p = subprocess.check_call(
            ['sort',
             '-k'
             '1,1',
             '-k'
             '2,2n',
             self.inputBedGeneric.name,
             '-o',
             self.sortedBedFile.name])

        # Before the bedToBigBed processing, we need to retrieve the chrom.sizes file from the reference genome
        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        self.twoBitFile = self.subtools.faToTwoBit(self.inputFastaFile.name, mySpecieFolderPath)

        # Generate the chrom.sizes
        # TODO: Isolate in a function
        # We first get the twoBit Infos
        try:
            p = subprocess.check_call(
                [os.path.join(ucsc_tools_path, 'twoBitInfo'),
                 self.twoBitFile.name,
                 self.twoBitInfoFile.name]
            )
        except subprocess.CalledProcessError:
            raise

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        try:
            p = subprocess.check_call(
                ['sort',
                 '-k2rn',
                 self.twoBitInfoFile.name,
                 '-o',
                 self.chromSizesFile.name])
        except subprocess.CalledProcessError:
            raise

        # bedToBigBed processing
        # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "bed.bb"

        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            try:
                p = subprocess.check_call(
                [os.path.join(ucsc_tools_path, 'bedToBigBed'),
                 self.sortedBedFile.name,
                 self.chromSizesFile.name,
                 bigBedFile.name])
            except subprocess.CalledProcessError:
                raise

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        # Return the BigBed track
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackName=trackName,
            longLabel='From Bed',
            shortLabel='bed file',
            trackDataURL=dataURL,
            trackType='bigBed',
            visibility='dense')

