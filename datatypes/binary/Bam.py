#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Class to handle Bam files to UCSC TrackHub
"""

import logging
import os
import shutil

from Binary import Binary
from datatypes.validators.DataValidation import DataValidation



class Bam(Binary):
    def __init__(self, input_bam_false_path, data_bam):
        super(Bam, self).__init__()
        self.inputFile = input_bam_false_path
        self.trackSettings = data_bam
        self.dataType = "bam"
        self.trackType = "bam"
        
    
    def initSettings(self):
        super(Bam, self).initSettings()
        if ".bam" not in self.trackName:
            self.trackName = self.trackName + ".bam"
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.trackSettings:
                self.extraSettings["color"] = self.trackSettings["track_color"]
        if "group_name" in self.trackSettings:
            self.extraSettings["group"] = self.trackSettings["group_name"]
        self.extraSettings["visibility"] = "pack"
        self.extraSettings["priority"] = self.trackSettings["order_index"]

    def validateData(self):
        self.validator = DataValidation(self.inputFile, self.dataType, self.chromSizesFile.name)
        self.validator.validate()
    
    def createTrack(self):
        super(Bam, self).createTrack()
        self._moveBamIndex()

    def _moveBamIndex(self):
        # Create and add the bam index file to the same folder
        self.index_bam = self.trackSettings["index"]
        name_index_bam = self.trackName + ".bai"
        bam_index_file_path = os.path.join(self.myTrackFolderPath, name_index_bam)
        shutil.copyfile(self.index_bam, bam_index_file_path)
        

