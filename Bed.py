#!/usr/bin/python

import os
import subprocess
import tempfile

# Internal dependencies
from twoBitCreator import twoBitFileCreator
from Track import Track


class Bed(object):
    def __init__(self, inputBedGeneric, inputFastaFile, outputFile, toolDirectory, extra_files_path, ucsc_tools_path, trackHub):
        super(Bed, self).__init__()

        self.track = None

        self.inputBedGeneric = inputBedGeneric
        self.inputFastaFile = inputFastaFile
        self.chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")
        self.twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)

        self.outputFile = outputFile
        self.toolDirectory = toolDirectory
        self.extra_files_path = extra_files_path
        self.ucsc_tools_path = ucsc_tools_path
        self.trackHub = trackHub

        # Before the bedToBigBed processing, we need to retrieve the chrom.sizes file from the reference genome
        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        twoBitFile = twoBitFileCreator(self.inputFastaFile, ucsc_tools_path, mySpecieFolderPath)

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
        self.twoBitInfoFile.write(twoBitInfo_out)

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        p = subprocess.Popen(
            ['sort',
             '-k2rn',
             self.twoBitInfoFile.name,
             '-o',
             self.chromSizesFile.name])
        p.wait()

        # bedToBigBed processing
        # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "bed.bb"
        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            p = subprocess.Popen(
                [os.path.join(ucsc_tools_path, 'bedToBigBed'),
                 self.inputBedGeneric.name,
                 self.chromSizesFile.name,
                 bigBedFile.name])
            p.wait()

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

