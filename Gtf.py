#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Gtf( Datatype ):
    def __init__( self, input_gtf_false_path, data_gtf,
                 input_fasta_file, extra_files_path, tool_directory ):
        super(Gtf, self).__init__( input_fasta_file=input_fasta_file,
                                   extra_files_path=extra_files_path,
                                   tool_directory=tool_directory )

        self.track = None

        self.input_gtf_false_path = input_gtf_false_path
        self.name_gtf = data_gtf["name"]
        self.priority = data_gtf["order_index"]

        print "Creating TrackHub GTF from (falsePath: %s; name: %s)" % ( self.input_gtf_false_path, self.name_gtf)

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        twoBitInfoFile = tempfile.NamedTemporaryFile(bufsize=0)
        chromSizesFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".chrom.sizes")

        # GtfToGenePred
        subtools.gtfToGenePred(self.input_gtf_false_path, genePredFile.name)

        # TODO: From there, refactor because common use with Gff3.py
        #  genePredToBed processing
        subtools.genePredToBed(genePredFile.name, unsortedBedFile.name)

        # Sort processing
        subtools.sort(unsortedBedFile.name, sortedBedFile.name)

        # TODO: Chehck if the twoBitInfo / ChromSizes is redundant and make an intermediate class
        # Generate the twoBitInfo
        subtools.twoBitInfo(self.twoBitFile.name, twoBitInfoFile.name)

        # Then we get the output to generate the chromSizes
        # TODO: Check if no errors
        subtools.sortChromSizes(twoBitInfoFile.name, chromSizesFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "".join( ( self.name_gtf, ".bb") )
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name, chromSizesFile.name, bigBedFile.name)

        # Create the Track Object
        dataURL = "tracks/%s" % trackName

        trackDb = TrackDb(
            trackName=trackName,
            longLabel=self.name_gtf,
            shortLabel=self.getShortName( self.name_gtf ),
            trackDataURL=dataURL,
            trackType='bigBed 12 +',
            visibility='dense',
            priority=self.priority,
        )
        self.track = Track(
            trackFile=myBigBedFilePath,
            trackDb=trackDb,
        )

        print("- %s created in %s" % (trackName, myBigBedFilePath))
