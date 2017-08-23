#!/usr/bin/python

import os
import tempfile
import string

from Datatype import Datatype
from util import subtools


class bigPsl( Datatype ):
    def __init__(self, input_bigpsl_false_path, data_bigpsl):

        super(bigPsl, self).__init__()
        self.inputBigPsl = input_bigpsl_false_path
        self.bigPslMetaData = data_bigpsl
        self.bedType = "bed12+12"
        self.trackType = "bigPsl"

    def generateCustomTrack(self):
        self.initBigPslSettings()
        self.convertBigPslTobigBed()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- BigPsl %s created" % self.trackName)

    def initBigPslSettings(self):  
        self.initRequiredSettings(self.bigPslMetaData, trackType = self.trackType) 
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.bigPslMetaData:
            self.extra_settings["track_color"] = self.bigPslMetaData["track_color"]
        if "group_name" in self.bigPslMetaData:
            self.extra_settings["group_name"] = self.bigPslMetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.bigPslMetaData["order_index"]
        if "database" in self.bigPslMetaData:
            self.extra_settings["database"] = self.bigPslMetaData["database"]

    def convertBigPslTobigBed(self):
        # Sort processing
        self.sortedBigPslFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        subtools.sort(self.inputBigPsl, self.sortedBigPslFile.name)
        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'bigPsl.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBigPslFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 typeOption=self.bedType,
                                 tab='True',
                                 autoSql=auto_sql_option,
                                 extraIndex='name'
                                 )