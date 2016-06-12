#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Bed( Datatype ):
    def __init__( self, inputBedGeneric, data_bed_generic,
                 inputFastaFile, extra_files_path, tool_directory ):
        super(Bed, self).__init__(
            inputFastaFile, extra_files_path, tool_directory
        )

        self.track = None

        self.inputBedGeneric = inputBedGeneric

        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        self.chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")
        self.twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)

        self.data_bed_generic = data_bed_generic
        self.name_bed_generic = self.data_bed_generic["name"]

        # Sort processing
        subtools.sort(self.inputBedGeneric, self.sortedBedFile.name)

        # Generate the chrom.sizes
        # TODO: Isolate in a function
        # We first get the twoBit Infos
        subtools.twoBitInfo(self.twoBitFile.name, self.twoBitInfoFile.name)

        # Then we get the output to inject into the sort
        # TODO: Check if no errors
        subtools.sortChromSizes(self.twoBitInfoFile.name, self.chromSizesFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "".join( ( self.name_bed_generic, ".bb") )

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name, self.chromSizesFile.name, self.bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        trackDb = TrackDb(
            trackName=trackName,
            longLabel=self.name_bed_generic,
            shortLabel=self.getShortName(self.name_bed_generic),
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
