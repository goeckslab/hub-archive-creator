#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Gff3( Datatype ):
    def __init__( self, input_Gff3_false_path, data_gff3,
                  input_fasta_false_path, extra_files_path, tool_directory ):
        super( Gff3, self ).__init__(
                input_fasta_false_path, extra_files_path, tool_directory
        )

        self.track = None

        self.input_Gff3_false_path = input_Gff3_false_path
        self.name_gff3 = data_gff3["name"]

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # TODO: Refactor into another Class to manage the twoBitInfo and ChromSizes (same process as in Gtf.py)
        twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
        chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

        # gff3ToGenePred processing
        subtools.gff3ToGenePred(self.input_Gff3_false_path, genePredFile.name)

        # TODO: From there, refactor because common use with Gtf.py
        # genePredToBed processing
        subtools.genePredToBed(genePredFile.name, unsortedBedFile.name)

        # Sort processing
        subtools.sort(unsortedBedFile.name, sortedBedFile.name)

        # Generate the twoBitInfo
        subtools.twoBitInfo(self.twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to generate the chromSizes
        # TODO: Check if no errors
        subtools.sortChromSizes(twoBitInfoFile.name, chromSizesFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "".join( (self.name_gff3, ".bb" ) )
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name, chromSizesFile.name, bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        trackDb = TrackDb(
            trackName=trackName,
            longLabel='From Gff3',
            shortLabel='GFF3 File',
            trackDataURL=dataURL,
            trackType='bigBed 12 +',
            visibility='dense',
        )

        self.track = Track(
            trackFile=myBigBedFilePath,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (trackName, myBigBedFilePath))
