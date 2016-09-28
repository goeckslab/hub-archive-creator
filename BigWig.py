#!/usr/bin/python

import os
import shutil

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb


class BigWig( Datatype ):
    def __init__(self, input_bigwig_path, data_bigwig):
        super(BigWig, self).__init__()

        self.track = None

        self.input_bigwig_path = input_bigwig_path
        self.name_bigwig = data_bigwig["name"]
        self.priority = data_bigwig["order_index"]
        self.track_color = data_bigwig["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = data_bigwig["group_name"]

        #print "Creating TrackHub BigWig from (falsePath: %s; name: %s)" % ( self.input_bigwig_path, self.name_bigwig )

        trackName = "".join( ( self.name_bigwig, ".bigwig" ) )

        myBigWigFilePath = os.path.join(self.myTrackFolderPath, trackName)
        shutil.copy(self.input_bigwig_path, myBigWigFilePath)

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_bigwig,
                         track_type='bigWig', visibility='full',
                         priority=self.priority,
                         track_file=myBigWigFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name)

        # dataURL = "tracks/%s" % trackName
        #
        # # Return the BigBed track
        #
        # trackDb = TrackDb(
        #     trackName=trackName,
        #     longLabel=self.name_bigwig,
        #     shortLabel=self.getShortName( self.name_bigwig ),
        #     trackDataURL=dataURL,
        #     trackType='bigWig',
        #     visibility='full',
        #     priority=self.priority,
        # )
        #
        # self.track = Track(
        #     trackFile=myBigWigFilePath,
        #     trackDb=trackDb,
        # )

        print("- BigWig %s created" % self.name_bigwig)
        #print("- %s created in %s" % (trackName, myBigWigFilePath))
