#!/usr/bin/python

import tempfile
import os

from util import subtools
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
        subtools.sort(inputBedSimpleRepeatsFile.name, sortedBedFile.name)

        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        twoBitFile = subtools.faToTwoBit(inputFastaFile.name, mySpecieFolderPath)

        # Generate the chrom.sizes

        # We first get the twoBit Infos
        subtools.twoBitInfo(twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        subtools.sortChromSizes(twoBitInfoFile.name, chromSizesFile.name)

        # bedToBigBed processing
        # bedToBigBed augustusDbia3.sortbed chrom.sizes augustusDbia3.bb
        # TODO: Find the best to get this path without hardcoding it
        myTrackFolderPath = os.path.join(mySpecieFolderPath, "tracks")
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = 'dbia3_trfBig.bb'
        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        auto_sql_option = "%s%s" % ('-as=', os.path.join(toolDirectory, 'trf_simpleRepeat.as'))
        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name, chromSizesFile.name, bigBedFile.name,
                                 typeOption='-type=bed4+12',
                                 autoSql=auto_sql_option)

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

        print("- %s created in %s" % (trackName, myBigBedFilePath))
