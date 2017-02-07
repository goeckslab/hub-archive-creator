#!/usr/bin/python

import os
import tempfile
import string

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class BedBlastAlignments( Datatype ):
    def __init__(self, input_bed_blast_alignments_false_path, data_bed_blast_alignments):

        super(BedBlastAlignments, self).__init__()

        self.input_bed_blast_alignments_false_path = input_bed_blast_alignments_false_path
        self.name_bed_blast_alignments = data_bed_blast_alignments["name"]
        self.priority = data_bed_blast_alignments["order_index"]
        self.track_color = data_bed_blast_alignments["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_bed_blast_alignments["group_name"]

        #sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # Sort processing
        #subtools.sort(self.input_bigpsl_false_path, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = "".join( ( self.name_bed_blast_alignments, '.bb' ) )

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(self.input_bed_blast_alignments_false_path,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 typeOption='bed12+12',
                                 tab='True',
                                 autoSql=auto_sql_option)

        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_bed_blast_alignments, track_type='bigBed 12 +', visibility='dense',
                         priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name)


        # dataURL = "tracks/%s" % trackName
        #
        # trackDb = TrackDb(
        #     trackName=trackName,
        #     longLabel=self.name_bed_simple_repeats,
        #     shortLabel=self.getShortName( self.name_bed_simple_repeats ),
        #     trackDataURL=dataURL,
        #     trackType='bigBed 4 +',
        #     visibility='dense',
        #     priority=self.priority,
        # )
        #
        # self.track = Track(
        #     trackFile=myBigBedFilePath,
        #     trackDb=trackDb,
        # )

        print("- Bed Blast alignments %s created" % self.name_bed_blast_alignments)
        #print("- %s created in %s" % (trackName, myBigBedFilePath))
