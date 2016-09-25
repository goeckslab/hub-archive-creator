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
        self.track_color = data_gtf["track_color"]

        #print "Creating TrackHub GTF from (falsePath: %s; name: %s)" % ( self.input_gtf_false_path, self.name_gtf)

        # TODO: See if we need these temporary files as part of the generated files
        genePredFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
        sorted_bigGenePred_file = tempfile.NamedTemporaryFile(suffix=".sortedBed.bigGenePred")

        # GtfToGenePred
        subtools.gtfToGenePred(self.input_gtf_false_path, genePredFile.name)

        # TODO: From there, refactor because common use with Gff3.py
        # genePredToBigGenePred processing
        subtools.genePredToBigGenePred(genePredFile.name, unsorted_bigGenePred_file.name)

        # Sort processing
        subtools.sort(unsorted_bigGenePred_file.name, sorted_bigGenePred_file.name)

        # bedToBigBed processing
        trackName = "".join( ( self.name_gtf, ".bb") )

        auto_sql_option = os.path.join(self.tool_directory, 'bigGenePred.as')

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sorted_bigGenePred_file.name,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 autoSql=auto_sql_option,
                                 typeOption='bed12+8',
                                 tab=True)


        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_gtf, track_type='bigGenePred',
                         visibility='dense', priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color)

        print("- Gtf %s created" % self.name_gtf)
