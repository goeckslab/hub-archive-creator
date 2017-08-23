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
        self.inputBigWig = input_bigwig_path
        self.bigWigMetaData = data_bigwig
        self.trackType = None

    def generateCustomTrack(self):
        self.initBigWigSettings()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- BigWig %s created" % self.trackName)  

    def initBigWigSettings(self):
        self.initRequiredSettings(self.bigWigMetaData) 
        self.trackName = "".join( ( self.trackName, ".bigwig" ) )
        self.moveBigWig()
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        self.trackType=self.determine_track_type(self.trackDataURL)
        if "track_color" in self.bigWigMetaData:
            self.extra_settings["track_color"] = self.bigWigMetaData["track_color"]
        if "group_name" in self.bigWigMetaData:
            self.extra_settings["group_name"] = self.bigWigMetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.bigWigMetaData["order_index"]

    def moveBigWig(self):
        myBigWigFilePath = os.path.join(self.myTrackFolderPath, self.trackName)
        shutil.copy(self.inputBigWig, myBigWigFilePath)
        
        
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
