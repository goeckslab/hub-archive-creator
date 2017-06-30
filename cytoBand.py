#!/usr/bin/python

import os
import tempfile

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class cytoBand( Datatype ):
    def __init__(self, input_bed_cytoBand_false_path, data_bed_cytoBand):

        super(cytoBand, self).__init__()

        self.input_bed_cytoBand_false_path = input_bed_cytoBand_false_path
        self.name_bed_cytoBand = data_bed_cytoBand["name"]
        self.priority = data_bed_cytoBand["order_index"]
        self.track_color = data_bed_cytoBand["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_bed_cytoBand["group_name"]
        self.database = data_bed_cytoBand["database"]
        if data_bed_cytoBand["long_label"]:
            self.long_label = data_bed_cytoBand["long_label"]
        else:
            self.long_label = self.name_bed_cytoBand
        sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # Sort processing
        subtools.sort(self.input_bed_cytoBand_false_path, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = "".join( ( self.name_bed_cytoBand, '.bb' ) )
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        auto_sql_option = os.path.join(self.tool_directory, 'cytoBandIdeo.as')

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 typeOption='bed4',
                                 autoSql=auto_sql_option)

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name='cytoBandIdeo',
                         long_label=self.long_label, 
                         track_type='bigBed',
                         visibility='dense',
                         priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name,
                         database=self.database)

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

        print("- Bed splice junctions %s created" % self.name_bed_cytoBand)
        #print("- %s created in %s" % (trackName, myBigBedFilePath))
