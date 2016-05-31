#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Bed(object):
    def __init__(self, inputBedGeneric, data_bed_generic, inputFastaFile, extra_files_path):
        super(Bed, self).__init__()

        self.track = None

        self.inputBedGeneric = inputBedGeneric

        self.inputFastaFile = inputFastaFile

        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        self.chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")
        self.twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)

        self.extra_files_path = extra_files_path

        # Sort processing
        subtools.sort(self.inputBedGeneric, self.sortedBedFile.name)

        # Before the bedToBigBed processing, we need to retrieve the chrom.sizes file from the reference genome
        mySpecieFolderPath = os.path.join(extra_files_path, "myHub", "dbia3")

        # 2bit file creation from input fasta
        self.twoBitFile = subtools.faToTwoBit(self.inputFastaFile, mySpecieFolderPath)

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
        trackName = "".join( ( data_bed_generic, ".bb") )

        myBigBedFilePath = os.path.join(myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name, self.chromSizesFile.name, self.bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        trackDb = TrackDb(
            trackName=trackName,
            longLabel='From Bed',  # TODO: Change this because it can be called by others thing that .bed => .gtf/.gff3
            shortLabel='bed file',
            trackDataURL=dataURL,
            trackType='bigBed',
            visibility='dense',
            thickDrawItem='on',
        )

        # Return the BigBed track
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (trackName, myBigBedFilePath))
