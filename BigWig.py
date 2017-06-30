#!/usr/bin/python

import os
import shutil
from subprocess import Popen, PIPE
import re

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
        self.database = data_bigwig["database"]
        if data_bigwig["long_label"]:
            self.long_label = data_bigwig["long_label"]
        else:
            self.long_label = self.name_bigwig
        #print "Creating TrackHub BigWig from (falsePath: %s; name: %s)" % ( self.input_bigwig_path, self.name_bigwig )

        trackName = "".join( ( self.name_bigwig, ".bigwig" ) )

        myBigWigFilePath = os.path.join(self.myTrackFolderPath, trackName)
        shutil.copy(self.input_bigwig_path, myBigWigFilePath)

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.long_label,
                         track_type=self.determine_track_type(myBigWigFilePath),
                         visibility='full',
                         priority=self.priority,
                         track_file=myBigWigFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name,
                         database = self.database)

        print("- BigWig %s created" % self.name_bigwig)
        #print("- %s created in %s" % (trackName, myBigWigFilePath))

    def determine_track_type(self, bw_file):
        """
        bigWig tracks must declare the expected signal range for the data
        (See https://genome.ucsc.edu/goldenpath/help/trackDb/trackDbHub.html).
        This method determines the range of values for a bigWig file using
        the bigWigInfo program.

        Implementation of reading from stdout is based on a Stackoverflow post:
        http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate

        :param bw_file: path to a bigWig file

        :returns: the bigWig track type
        """
        cmd_ph = Popen(["bigWigInfo", "-minMax", bw_file],
                       stdout=PIPE, bufsize=1)

        with cmd_ph.stdout:
            for line in iter(cmd_ph.stdout.readline, b''):
                bw_type = "bigWig %s" % line.rstrip()

        cmd_ph.wait()

        return bw_type
