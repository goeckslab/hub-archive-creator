#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Gff3( Datatype ):
    def __init__(self, input_Gff3_false_path, data_gff3):
        super( Gff3, self ).__init__()

        self.track = None

        self.input_Gff3_false_path = input_Gff3_false_path
        self.name_gff3 = data_gff3["name"]
        self.priority = data_gff3["order_index"]
        self.track_color = data_gff3["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_gff3["group_name"]

        # TODO: See if we need these temporary files as part of the generated files
        unsorted_genePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        unsorted_bigGenePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsorted.bigGenePred")
        sorted_biGenePred_file = tempfile.NamedTemporaryFile(suffix=".sorted.bigGenePred")

        # gff3ToGenePred processing
        subtools.gff3ToGenePred(self.input_Gff3_false_path, unsorted_genePred_file.name)

        # genePredToBigGenePred
        subtools.genePredToBigGenePred(unsorted_genePred_file.name, unsorted_bigGenePred_file.name)

        # Sort processing
        subtools.sort(unsorted_bigGenePred_file.name, sorted_biGenePred_file.name)

        # TODO: Check if no errors

        # bedToBigBed processing
        trackName = "".join( (self.name_gff3, ".bb" ) )

        auto_sql_option = os.path.join(self.tool_directory, 'bigGenePred.as')

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sorted_biGenePred_file.name,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 autoSql=auto_sql_option,
                                 typeOption='bed12+8',
                                 tab=True)

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_gff3,
                         track_type='bigGenePred', visibility='dense',
                         priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name)

        print("- Gff3 %s created" % self.name_gff3)
