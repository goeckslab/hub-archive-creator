#!/usr/bin/python

import os
import tempfile

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class BedSpliceJunctions( Datatype ):
    def __init__(self, input_bed_splice_junctions_false_path, data_bed_splice_junctions):

        super(BedSpliceJunctions, self).__init__()

        self.input_bed_splice_junctions_false_path = input_bed_splice_junctions_false_path
        self.name_bed_splice_junctions = data_bed_splice_junctions["name"]
        self.priority = data_bed_splice_junctions["order_index"]
        self.track_color = data_bed_splice_junctions["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_bed_splice_junctions["group_name"]
        if data_bed_splice_junctions["long_label"]:
            self.long_label = data_bed_splice_junctions["long_label"]
        else:
            self.long_label = self.name_bed_splice_junctions
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # Sort processing
        subtools.sort(self.input_bed_splice_junctions_false_path, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = "".join( ( self.name_bed_splice_junctions, '.bb' ) )
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        auto_sql_option = os.path.join(self.tool_directory, 'spliceJunctions.as')

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 typeOption='bed12+1',
                                 autoSql=auto_sql_option)

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.long_label, track_type='bigBed 12 +', visibility='dense',
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

        print("- Bed splice junctions %s created" % self.name_bed_splice_junctions)
        #print("- %s created in %s" % (trackName, myBigBedFilePath))
