#!/usr/bin/python

import tempfile
import subprocess
import os

from twoBitCreator import twoBitFileCreator
from Track import Track


class BedSimpleRepeats(object):
    def __init__(self, inputBedSimpleRepeatsFile, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub):
        super(BedSimpleRepeats, self).__init__()

        inputBedSimpleRepeatsFile = open(inputBedSimpleRepeatsFile, 'r')
        inputFastaFile = open(inputFastaFile, 'r')

        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
        chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

        # Sort processing
        p = subprocess.Popen(
            ['sort',
                '-k'
                '1,1',
                '-k'
                '2,2n',
                inputBedSimpleRepeatsFile.name,
                '-o',
                sortedBedFile.name])
        p.wait()

        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        twoBitFile = twoBitFileCreator(inputFastaFile, ucsc_tools_path, mySpecieFolderPath)

        # Generate the chrom.sizes
        # TODO: Isolate in a function
        # We first get the twoBit Infos
        p = subprocess.Popen(
            [os.path.join(ucsc_tools_path, 'twoBitInfo'),
                twoBitFile.name,
                'stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        twoBitInfo_out, twoBitInfo_err = p.communicate()
        twoBitInfoFile.write(twoBitInfo_out)

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        p = subprocess.Popen(
            ['sort',
                '-k2rn',
                twoBitInfoFile.name,
                '-o',
                chromSizesFile.name])
        p.wait()

        # bedToBigBed processing
        # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
        # TODO: Find the best to get this path without hardcoding it
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = 'dbia3_trfBig.bb'
        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            p = subprocess.Popen(
                [os.path.join(ucsc_tools_path, 'bedToBigBed'),
                    '-type=bed4+12',
                    "%s%s" % ('-as=', os.path.join(toolDirectory, 'trf_simpleRepeat.as')),
                    sortedBedFile.name,
                    chromSizesFile.name,
                    bigBedFile.name])
            p.wait()

        # Create the Track Object
        dataURL = "tracks/%s" % trackName
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackName=trackName,
            longLabel='Tandem Repeats Big by TrfBig',
            shortLabel='Tandem Repeats',
            trackDataURL=dataURL,
            trackType='bigBed 4 +',
            visibility='dense'
        )
