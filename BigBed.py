#!/usr/bin/python

import os
import shutil
from subprocess import Popen, PIPE
import re

# Internal dependencies
from Datatype import Datatype

class BigBed(Datatype):
    """ Configurations for creating the bigBed evidence track """

    def __init__(self, input_bigbed_path, data_bigbed):
        super(BigBed, self).__init__()
        self.inputBigBed = input_bigbed_path
        self.bigBedMetaData = data_bigbed
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
        print("- BigBed %s created" % self.trackName)  

    def initBigWigSettings(self):
        self.initRequiredSettings(self.bigBedMetaData) 
        self.trackName = "".join( ( self.trackName, ".bigbed" ) )
        self.moveBigBed()
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        self.trackType=self.determine_track_type(self.trackDataURL)
        if "track_color" in self.bigBedMetaData:
            self.extra_settings["track_color"] = self.bigBedMetaData["track_color"]
        if "group_name" in self.bigBedMetaData:
            self.extra_settings["group_name"] = self.bigBedMetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.bigBedMetaData["order_index"]
        if "database" in self.bigBedMetaData:
            self.extra_settings["database"] = self.bigBedMetaData["database"]
    
    def moveBigBed(self):
        myBigBedFilePath = os.path.join(self.myTrackFolderPath, self.trackName)
        shutil.copy(self.inputBigBed, myBigBedFilePath)

    def determine_track_type(self, bb_file):
        """
        Determine the number of standard and extra fields using bigBedSummary

        Implementation of reading from stdout is based on a Stackoverflow post:
        http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate

        :param bb_file: path to a bigBed file

        :returns: the bigBed track type
        """

        cmd_ph = Popen(["bigBedSummary", "-fields", bb_file, "stdout"],
                       stdout=PIPE, bufsize=1)

        pattern = r"(\d+) bed definition fields, (\d+) total fields"

        with cmd_ph.stdout:
            for line in iter(cmd_ph.stdout.readline, b''):
                match = re.match(pattern, line)

                if match:
                    extra_mark = "." if match.group(1) == match.group(2) else "+"
                    bed_type = "bigBed %s %s" % (match.group(1), extra_mark)
                    break

        cmd_ph.wait()

        return bed_type
