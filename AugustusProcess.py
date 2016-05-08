#!/usr/bin/python

import tempfile
import subprocess
import os

# Internal dependencies
from twoBitCreator import twoBitFileCreator
from Track import Track
from util.SubTools import SubTools


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

        # TODO: Check the SubTools object
        self.subTools = SubTools()

        # gff3ToGenePred processing
        self.subTools.gff3ToGenePred(inputGFF3File.name, genePredFile.name)

        # genePredToBed processing
        try:
            p = subprocess.check_call(
                [os.path.join(ucsc_tools_path, 'genePredToBed'),
                 genePredFile.name,
                 unsortedBedFile.name])
        except subprocess.CalledProcessError:
            raise

        # Sort processing
        try:
            p = subprocess.check_call(
                ['sort',
                 '-k'
                 '1,1',
                 '-k'
                 '2,2n',
                 unsortedBedFile.name,
                 '-o',
                 sortedBedFile.name])
        except subprocess.CalledProcessError:
            raise

        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        twoBitFile = twoBitFileCreator(inputFastaFile, ucsc_tools_path, mySpecieFolderPath)

        # Generate the chrom.sizes
        self.subTools.twoBitInfo(twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        try:
            p = subprocess.check_call(
                ['sort',
                 '-k2rn',
                 twoBitInfoFile.name,
                 '-o',
                 chromSizesFile.name])
        except subprocess.CalledProcessError:
            raise

        # bedToBigBed processing
        # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
        # TODO: Find the best to get this path without hardcoding it
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "augustusDbia3.bb"
        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            try:
                p = subprocess.check_call(
                    [os.path.join(ucsc_tools_path, 'bedToBigBed'),
                     sortedBedFile.name,
                     chromSizesFile.name,
                     bigBedFile.name])
            except subprocess.CalledProcessError:
                raise

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
