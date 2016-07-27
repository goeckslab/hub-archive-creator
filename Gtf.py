#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Gtf( Datatype ):
    def __init__( self, input_gtf_false_path, data_gtf):

        super(Gtf, self).__init__()

        self.track = None

        self.input_gtf_false_path = input_gtf_false_path
        self.name_gtf = data_gtf["name"]
        self.priority = data_gtf["order_index"]

        #print "Creating TrackHub GTF from (falsePath: %s; name: %s)" % ( self.input_gtf_false_path, self.name_gtf)

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # GtfToGenePred
        subtools.gtfToGenePred(self.input_gtf_false_path, genePredFile.name)

        # TODO: From there, refactor because common use with Gff3.py
        #  genePredToBed processing
        subtools.genePredToBed(genePredFile.name, unsortedBedFile.name)

        # Sort processing
        subtools.sort(unsortedBedFile.name, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "".join( ( self.name_gtf, ".bb") )
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name, self.chromSizesFile.name, bigBedFile.name)

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

        #print("- %s created in %s" % (trackName, myBigBedFilePath))
