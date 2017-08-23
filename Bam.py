#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Class to handle Bam files to UCSC TrackHub
"""

import logging
import os
import shutil

from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb



class Bam( Datatype ):
    def __init__(self, input_bam_false_path, data_bam):
        super(Bam, self).__init__()
        self.inputBam = input_bam_false_path
        self.bamMetaData = data_bam
        self.trackType = "bam"
        
    def generateCustomTrack(self):
        self.initBamSettings()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- Bam %s created" % self.trackName)  

    def initBamSettings(self):
        self.initRequiredSettings(self.bamMetaData, trackType = self.trackType) 
        self.moveBam()
        self.moveBamIndex()
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.bamMetaData:
            self.extra_settings["track_color"] = self.bamMetaData["track_color"]
        if "group_name" in self.bamMetaData:
            self.extra_settings["group_name"] = self.bamMetaData["group_name"]
        self.extra_settings["visibility"] = "pack"
        self.extra_settings["priority"] = self.bamMetaData["order_index"]

    def moveBam(self):
        if ".bam" not in self.trackName:
            self.trackName = self.trackName + ".bam"
        bam_file_path = os.path.join(self.myTrackFolderPath, self.trackName)
        shutil.copyfile(self.inputBam, bam_file_path)
    
    def moveBamIndex(self):
        # Create and add the bam index file to the same folder
        self.index_bam = self.bamMetaData["index"]
        name_index_bam = self.trackName + ".bai"
        bam_index_file_path = os.path.join(self.myTrackFolderPath, name_index_bam)
        shutil.copyfile(self.index_bam, bam_index_file_path)
