#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from util import subtools


class Bed( Datatype ):
    def __init__( self, inputBedGeneric, data_bed_generic):
        super(Bed, self).__init__()
        self.inputBed = inputBedGeneric
        self.bedMetaData = data_bed_generic
        self.trackType = "bigBed"
        
    def generateCustomTrack(self):
        self.initBedSettings()
        self.convertBedTobigBed()
        # Create the Track Object
        self.createTrack(trackName=self.trackName,
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- Bed %s created" % self.trackName)  
      
    def initBedSettings(self):
        self.initRequiredSettings(self.bedMetaData, trackType = self.trackType) 
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        self.trackName = "".join( ( self.trackName, ".bb") )
        self.trackDataURL = os.path.join(self.myTrackFolderPath, self.trackName)
        if "track_color" in self.bedMetaData:
            self.extra_settings["track_color"] = self.bedMetaData["track_color"]
        if "group_name" in self.bedMetaData:
            self.extra_settings["group_name"] = self.bedMetaData["group_name"]
        self.extra_settings["visibility"] = "dense"
        self.extra_settings["priority"] = self.bedMetaData["order_index"]
        
    def convertBedTobigBed(self):
        # Sort processing
        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        subtools.sort(self.inputBed, self.sortedBedFile.name)
        # bedToBigBed processing
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 )
        #print("- Bed %s created" % self.trackName)


