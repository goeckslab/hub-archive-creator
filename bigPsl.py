#!/usr/bin/python

import os
import tempfile
import string

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class bigPsl( Datatype ):
    def __init__(self, input_bigpsl_false_path, data_bigpsl):

        super(bigPsl, self).__init__()

        self.input_bigpsl_false_path = input_bigpsl_false_path
        self.name_bigpsl = data_bigpsl["name"]
        self.priority = data_bigpsl["order_index"]
        self.track_color = data_bigpsl["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_bigpsl["group_name"]

        #sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # Sort processing
        #subtools.sort(self.input_bigpsl_false_path, sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + .bb
        trackName = "".join( ( self.name_bigpsl, '.bb' ) )

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(self.input_bigpsl_false_path,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 typeOption='bed12+12',
                                 tab='True',
                                 autoSql=auto_sql_option)

        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_bigpsl, track_type='bigPsl', visibility='dense',
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

        print("- bigPsl %s created" % self.name_bigpsl)
        #print("- %s created in %s" % (trackName, myBigBedFilePath))
