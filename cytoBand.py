#!/usr/bin/python

import os
import tempfile

from Bed import Bed
from util import subtools


class cytoBand( Bed ):
    def __init__(self, input_bed_cytoBand_false_path, data_bed_cytoBand):

        super(cytoBand, self).__init__(input_bed_cytoBand_false_path, data_bed_cytoBand)
        self.bedType ="bed4+1"
        self.trackType = "bigBed"
        
    def generateCustomTrack(self):
        self.initBedSettings()
        self.convertBedTobigBed()
        # Create the Track Object
        self.createTrack(trackName='cytoBandIdeo',
                         longLabel=self.longLabel, 
                         shortLabel=self.shortLabel,
                         trackDataURL=self.trackDataURL,
                         trackType=self.trackType,
                         extra_settings = self.extra_settings
        )
        print("- Bed %s created" % self.trackName)  

    def convertBedTobigBed(self):
        # Sort processing
        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")
        subtools.sort(self.inputBed, self.sortedBedFile.name)
        # bedToBigBed processing
        auto_sql_option = os.path.join(self.tool_directory, 'cytoBandIdeo.as')
        with open(self.trackDataURL, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name,
                                 typeOption=self.bedType,
                                 tab='True',
                                 autoSql=auto_sql_option
                                 )
       